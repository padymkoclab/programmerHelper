
import string
import random
import io

from django.utils import timezone
from django.core.files.base import ContentFile
from django.template import Template, Context

from PIL import ImageColor, ImageDraw, Image
import factory
from factory import fuzzy

from ..python.text_utils import findall_words


class AbstractTimeStampedFactory(factory.DjangoModelFactory):

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        super()._after_postgeneration(obj, create, results)
        qs = obj._meta.model._default_manager.filter(pk=obj.pk)
        try:
            updated = fuzzy.FuzzyDateTime(obj.created, timezone.now()).fuzz()
            qs.update(updated=updated)
        except Exception as e:
            import ipdb; ipdb.set_trace()

    @factory.post_generation
    def created(self, create, extracted, **kwargs):
        self.created = fuzzy.FuzzyDateTime(timezone.now() - timezone.timedelta(days=500)).fuzz()
        self.save()


def generate_image(width=100, height=100, filename='setivolkylany', imageformat='JPEG', show=False):
    """Generate image by help Pillow on based width, height and image`s format."""

    # generate supported the PIL`s colors in RGB
    colors = [ImageColor.getrgb(colorname) for colorname in ImageColor.colormap.keys()]

    # choice a random color
    color = random.choice(colors)

    # create a buffer for an image
    buffer_file = io.BytesIO()

    # create an image
    image = Image.new('RGB', (width, height), color)

    # draw a text by center on the image if it possible contains it
    draw = ImageDraw.Draw(image)
    text = '{0} X {1}'.format(width, height)
    textwidth, textheight = draw.textsize(text)
    if textwidth < width and textheight < height:
        left = (width - textwidth) // 2
        top = (height - textheight) // 2
        draw.text((left, top), text, fill=(0, 0, 0))

    # write the image in buffer
    image.save(buffer_file, imageformat)

    # show the image if needed
    if show:
        image.show()

    # write the generated image in supported the Django`s type and return it
    buffer_file.seek(0)
    imagecontent = buffer_file.getvalue()
    image = ContentFile(imagecontent, filename)
    return image


def generate_text_by_min_length(min_length, as_p=False):
    """Generate random text by minumim length.
    If parameter 'as_p' is true, at that time text will be as HTML paragraph."""

    # validation input
    if not isinstance(min_length, int):
        raise TypeError('Min length text must positive integer, not {0}'.format(type(min_length)))
    if min_length < 1:
        raise ValueError('Min length text must positive integer, not {0}'.format(min_length))
    # initialization
    method = 'p' if as_p is True else ''
    text = str()
    counter_iterations = 1
    # populate text
    while min_length > len(text):
        pattern = '{% lorem ' + str(counter_iterations) + ' ' + method + ' random %}'
        block_text = Template(pattern).render(Context())
        text = '{0}\n\n{1}'.format(text, block_text).strip()
        counter_iterations += 1
    return text


def generate_text_certain_length(length, locale='en'):
    """Generate text certain length with full-featured sentences."""

    # generate random text
    text = generate_text_by_min_length(length)
    assert len(text) >= length
    if len(text) == length:
        return text
    # make text approximate certain length
    while len(text) < length:
        text = text + ' ' + factory.Faker('text', locale=locale).generate([])
    # made full-fetured ending text for last sentence
    if len(text) != length:
        # slice text to certain length
        text = text[:length]
        # find last next-to-last sentence, if is
        next_to_last_sentence = text.rfind('.', 0, -1)
        if next_to_last_sentence != -1:
            # made lower ending last sentence and remove next-to-last point
            ending = text[next_to_last_sentence:].lower()
            text = text[:next_to_last_sentence] + ending[1:]

        # replace last space (if is) on character
        if text[-1] == ' ':
            text = text[:-1] + random.choice(string.ascii_lowercase)

        # replace next-to-last space (if is) on character
        if len(text) > 1 and text[-2] == ' ':
            text = text[:-2] + random.choice(string.ascii_lowercase) + text[-1]

        # replace last point (if is) on character
        if text[-1] == '.':
            text = text[:-1] + random.choice(string.ascii_lowercase)
    if len(text) == length:
        text = text[:-1]

    # set point in ending of sentence
    text += '.'
    return text


def generate_words(min_count_words, max_count_words, to_register='capitalize', locale='en'):
    """
    Generate words separated commas by passed count min and max needed words.
    Returned words may be as capitalize, upper, lower or title of each.
    Word may can contains unicode or ascii letters and controling with parameter 'locale'.

    >>> words = generate_words(1, 3)
    >>> len(words) in [1, 2, 3]
    True
    >>> words = generate_words(60, 60)
    >>> len(words) == 60
    True
    """

    #
    # Validation of input
    #

    # limiters must be integer
    if not (isinstance(min_count_words, int) and isinstance(max_count_words, int)):
        raise ValueError('Values \'min_count_words\' and \'max_count_words\' must be integer.')

    # min limiter must not great max limiter
    if min_count_words > max_count_words:
        raise ValueError('Min limiter count of the words must be not great than max limiter count of a words.')

    # limiters must be more than 0
    if not (min_count_words > 0 and max_count_words > 0):
        raise ValueError('Values \'min_count_words\' and \'max_count_words\' must be 1 or more.')

    # validate values of parameter 'to_register'
    if to_register not in ['capitalize', 'lower', 'title', 'upper']:
        raise ValueError("Values register of words must be 'capitalize', 'lower', 'title' or 'upper'.")

    # validate values of parameter 'locale'
    if locale not in ['ru', 'en']:
        raise ValueError(
            "Words may can generated only on English or Russian ('en' or 'ru'). Set 'locale' to 'ru' or 'en'."
        )

    #
    # Generate words
    #

    # generate random text with regards locale and getting words more or equal max needed
    random_words = list()
    while len(random_words) < max_count_words:
        text = factory.Faker('text', locale=locale).generate(())
        detected_words = findall_words(text)
        random_words.extend(detected_words)

    # slice determined count random_words
    number_for_slice = random.randint(min_count_words, max_count_words)
    slices_random_words = random_words[:number_for_slice]

    # applying function 'to_register' for each word
    words = list()
    for i, word in enumerate(slices_random_words):
        word = eval('"{word}".{function}()'.format(word=word, function=to_register))
        if to_register == 'capitalize' and i > 0:
            word = word.lower()
        words.append(word)
    return words


def random_text(count_sentences=3):
    """
    Analogy familiar 'Lorem', but realized on the pure Python.

    >>> random_text = random_text()
    >>> len(random_text.split('.'))
    3
    >>> random_text = random_text(78)
    >>> len(random_text.split('.'))
    78
    >>> random_text = random_text(2)
    >>> len(random_text.split('.'))
    2
    >>> random_text = random_text(1)
    >>> lst = random_text.split('.')
    >>> len(lst)
    2
    >>> lst[1]
    ''
    >>> random_text.count('.')
    1
    >>> random_text = random_text(0)
    >>> len(random_text)
    0
    >>> random_text
    ''
    >>> random_text = random_text(-1)
    >>> len(random_text)
    0
    >>> random_text
    ''
    """

    # make triple an all ascii-lower letters,
    # for ability a choice one character not once in word
    TRIPLE_CHARS = string.ascii_lowercase * 3

    # a list all a generated sentences
    sentences = list()

    # generate sentences
    for i in range(count_sentences):

        # list an all words in a sentence
        sentence = list()

        # random count a words in the sentence
        count_words_in_sentence = random.randint(3, 30)

        # generate words
        for j in range(count_words_in_sentence):

            # random length of a word
            word_length = random.randint(1, 20)

            # generate word by length
            for k in range(word_length):

                # a list of a chars, used in the word
                list_chars_in_words = random.sample(TRIPLE_CHARS, word_length)

                # make the list of the chars to string
                word = ''.join(list_chars_in_words)

            # add the word to the sentence
            sentence.append(word)

        # make the sentence from list to string, where a words will be separated by the gap
        sentence = ' '.join(sentence)

        # the sentence must be begin from a word with a big first letter
        sentence = sentence.capitalize()

        # the sentence must be end at the point
        sentence = sentence + '.'

        # add the sentence to the list of sentences
        sentences.append(sentence)

    # make the list of sentences to string, where an each sentence will be separated by the gap
    sentences = ' '.join(sentences)

    # return random text
    return sentences


def generate_text_random_length_for_field_of_model(factory, field_name, ending_chart='', locale='ru'):

    if ending_chart and len(ending_chart) != 1:
        raise ValueError('Length of a ending character must be equal 1.')

    model = factory._LazyStub__model_class._meta.model

    field = model._meta.get_field(field_name)

    min_length = 1
    max_length = 1000

    for validator in field.validators:
        if validator.code == 'min_length':
            min_length = validator.limit_value
        elif validator.code == 'max_length':
            max_length = validator.limit_value

    length = random.randrange(min_length, max_length)

    text = generate_text_certain_length(length, locale)

    if ending_chart:
        text = text[:-1] + ending_chart

    return text
