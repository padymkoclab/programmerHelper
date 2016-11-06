
import logging
import statistics
import uuid
import collections

from django.contrib.postgres.fields import ArrayField
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.python.utils import flatten
from utils.django.models_utils import get_admin_url, upload_image
from utils.django.models_fields import ConfiguredAutoSlugField, CountryField
from utils.django.models import TimeStampedModel
from utils.django.functions_db import Round
from utils.django.validators import OnlyLettersValidator

from apps.tags.models import Tag
from apps.tags.managers import TagManager
from apps.tags.mixins_models import TagModelMixin

from .managers import BookManager, WriterManager, PublisherManager


logger = logging.getLogger('django.development')

logger.info('Idea: announs book, soon')
logger.info('Idea: read with Scrapy data from Amazon.com')
logger.info('Idea: display language name on Site Language for user')
logger.info('Idea: I read it and I read it now and I want read it')

NOW_YEAR = timezone.now().year


class Book(TagModelMixin, models.Model):
    """
    Model for books
    """

    MIN_YEAR_PUBLISHED = 1950

    LANGUAGES = tuple((code, _(name)) for code, name in settings.LANGUAGES)

    def upload_book_image(instance, filename):
        return upload_image(instance, filename)

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(
        _('name'), max_length=100,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)],
        unique=True,
    )
    slug = ConfiguredAutoSlugField(populate_from='name', unique=True)
    description = models.TextField(
        _('description'), validators=[MinLengthValidator(100)],
    )
    image = models.ImageField(_('image'), upload_to=upload_book_image, max_length=1000)
    language = models.CharField(_('language'), max_length=10, choices=LANGUAGES, default='en')
    count_pages = models.PositiveSmallIntegerField(
        _('count pages'), validators=[MinValueValidator(1)]
    )
    authorship = models.ManyToManyField(
        'Writer',
        verbose_name=_('Authorship'),
        related_name='books',
    )
    publisher = models.ForeignKey(
        'Publisher', verbose_name=_('publisher'), related_name='books'
    )
    isbn = models.CharField(
        _('ISBN'), max_length=30, default='',
        help_text=_('ISBN code of a book'),
        validators=[
            RegexValidator(
                regex='\d+-\d+-\d+-\d+-\d+',
                message=_('Not correct ISBN for a book'),
            )
        ],
    )
    year_published = models.PositiveSmallIntegerField(
        _('Year published'),
        validators=[
            MinValueValidator(
                MIN_YEAR_PUBLISHED,
                _('Book doesn`t possible will published early than {0}.'.format(
                    MIN_YEAR_PUBLISHED
                ))
            ),
            MaxValueValidator(
                NOW_YEAR, _('Book doesn`t possible will published in future.')
            ),
        ]
    )
    created = models.DateTimeField(_('date added'), auto_now_add=True)
    tags = models.ManyToManyField(
        Tag, verbose_name=_('tags'), related_name='books',
    )

    objects = models.Manager()
    objects = BookManager()

    tags_manager = TagManager()

    class Meta:
        verbose_name = _("book")
        verbose_name_plural = _("books")
        get_latest_by = 'year_published'
        ordering = ['year_published']

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('books:book', kwargs={'slug': self.slug})

    def get_admin_url(self):
        return get_admin_url(self)

    def is_new(self):
        """This book published in this year or one year ago."""

        return self in self.__class__.objects.new_books()
    is_new.admin_order_field = 'year_published'
    is_new.short_description = _('Is new')
    is_new.boolean = True

    def get_size_display(self):
        """Getting size of books on based count pages."""

        size = self.__class__.objects.books_with_sizes().get(pk=self.pk).size

        if size == 'tiny':
            return _('Tiny')
        elif size == 'middle':
            return _('Middle')
        elif size == 'big':
            return _('Big')
        elif size == 'great':
            return _('Great')
    get_size_display.admin_order_field = 'count_pages'
    get_size_display.short_description = _('Size')

    def get_image_thumbnail(self):
        return format_html('<image src={0} />', self.image.url)
    get_image_thumbnail.short_description = _('Picture')

    def get_count_replies(self):
        """ """

        if hasattr(self, 'count_replies'):
            return self.count_replies

        return self.replies.count()
    get_count_replies.admin_order_field = 'count_replies'
    get_count_replies.short_description = _('Count replies')

    def get_rating(self):
        """Getting rating of book on based marks."""

        if hasattr(self, 'rating'):
            return self.rating

        replies_with_total_mark = self.replies.replies_with_total_mark()
        rating = replies_with_total_mark.aggregate(rating=models.Avg('total_mark'))['rating']
        if rating is not None:
            return round(rating, 3)
        return
    get_rating.admin_order_field = 'rating'
    get_rating.short_description = _('Rating')

    def get_most_common_words_from_replies(self):
        """Determining most common words presents in replies."""

        # get all words in advantages and disadvantages of reply as two-nested list
        all_words = self.replies.values_list('advantages', 'disadvantages')

        # flat the two-nested list to single list
        all_words = flatten(all_words)

        # get 10 most common words with counters
        most_common_words = collections.Counter(all_words).most_common(10)

        # leave only words, without counters
        return ', '.join(i for i, j in most_common_words)
    get_most_common_words_from_replies.short_description = _('Most common words from replies')


class Writer(models.Model):
    """
    Model for writers of books
    """

    MIN_BIRTH_YEAR = 1900
    MAX_BIRTH_YEAR = NOW_YEAR - 16
    MIN_DEATH_YEAR = 1916

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(
        _('Name'),
        max_length=200,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)],
        unique=True,
        error_messages={'unique': _('Writer with this name already exists.')}
    )
    slug = ConfiguredAutoSlugField(populate_from='name', unique=True)
    trends = ArrayField(
        models.CharField(max_length=100),
        size=10,
        help_text=_('Make listing words separated commas.')
    )
    about = models.TextField(
        _('About writer'),
        validators=[MinLengthValidator(100)],
        help_text=_('Give a brief character of the writer and his books.')
    )

    birth_year = models.PositiveSmallIntegerField(
        _('Year of birth'),
        validators=[
            MinValueValidator(MIN_BIRTH_YEAR, 'Writer not possible born early than {0} year.'.format(MIN_BIRTH_YEAR)),
            MaxValueValidator(MIN_BIRTH_YEAR, 'Writer not possible born late than {0} year.'.format(MAX_BIRTH_YEAR))
        ],
    )
    death_year = models.PositiveSmallIntegerField(
        _('Year of death'),
        null=True,
        blank=True,
        validators=[
            MinValueValidator(MIN_DEATH_YEAR, 'Writer not possible dead early than {0} year.'.format(MIN_DEATH_YEAR)),
            MaxValueValidator(NOW_YEAR, 'Writer not possible dead in future')
        ],
    )

    class Meta:
        verbose_name = _('Writer')
        verbose_name_plural = _('Writers')
        ordering = ['name']

    objects = models.Manager()
    objects = WriterManager()

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('books:writer', kwargs={'slug': self.slug})

    def get_admin_url(self):
        return reverse('admin:books_writer_change', args=(self.pk, ))

    def clean(self):

        if self.death_year is not None:
            if self.death_year - self.birth_year < 16:
                raise ValidationError({'__all__': _('Too less range between birth and death years.')})

    def get_count_books(self):
        """ """

        if hasattr(self, 'count_books'):
            return self.count_books

        return self.books.count()
    get_count_books.admin_order_field = 'count_books'
    get_count_books.short_description = _('Count books')

    def get_age(self):
        """Getting age writer if it is possible."""

        if hasattr(self, 'age'):
            return self.age

        if self.death_year is None:
            return NOW_YEAR - self.birth_year
        return self.death_year - self.birth_year
    get_age.short_description = _('Age')
    get_age.admin_order_field = 'age'

    def get_years_life(self):
        """Return years of life of writer, replace 0 on sign '?'."""

        return '{0} - {1}'.format(self.birth_year, '' if self.death_year is None else self.death_year)
    get_years_life.short_description = _('Year life')

    def is_alive_writer(self):
        """Return boolean - this writer now is living?"""

        if hasattr(self, 'is_alive'):
            return self.is_alive

        if self.death_year is None:
            return True
        return False
    is_alive_writer.short_description = _('Is alive?')
    is_alive_writer.admin_order_field = 'is_alive'
    is_alive_writer.boolean = True

    def get_avg_mark_for_books(self):
        """Getting avarage mark for books`s writer, on based average rating it books."""

        if hasattr(self, 'avg_mark_for_books'):
            return self.avg_mark_for_books

        if self.books.exists():
            books_with_rating = self.books.books_with_rating()
            # return books_with_rating.aggregate(
            #     avg=Round(
            #         models.Avg('rating')
            #     )
            # )['avg']
            values = books_with_rating.values_list('rating', flat=True)
            values = (i or 0 for i in values)
            avg_mark_for_books = statistics.mean(values)
            return round(avg_mark_for_books, 3)
        return
    get_avg_mark_for_books.short_description = _('Average mark for books')
    get_avg_mark_for_books.admin_order_field = 'avg_mark_for_books'


class Publisher(models.Model):

    MIN_FOUNDED_YEAR = 1900

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(
        _('name'), max_length=50, unique=True,
        error_messages={'unique': _('Publisher with this name already exists.')}
    )
    slug = ConfiguredAutoSlugField(populate_from='name', unique=True)
    country_origin = CountryField()
    headquarters = models.CharField(_('headquarters'), max_length=50)
    founded_year = models.PositiveSmallIntegerField(
        _('Founded year'),
        validators=[
            MinValueValidator(
                MIN_FOUNDED_YEAR,
                _('Publishing company not possible founded early than {}'.format(MIN_FOUNDED_YEAR))
            ),
            MaxValueValidator(NOW_YEAR, _('Publishing company not possible founded in future')),
        ])
    website = models.URLField(_('Official website'))

    objects = models.Manager()
    objects = PublisherManager()

    class Meta:
        verbose_name = _('Publisher')
        verbose_name_plural = _('Publishers')
        ordering = ['name']

    def __str__(self):
        return '{0}'.format(self.name)

    def get_absolute_url(self):
        return reverse('books:publisher', kwargs={'slug': self.slug})

    def get_admin_url(self):
        return get_admin_url(self)

    def get_count_books(self):
        """ """

        if hasattr(self, 'count_books'):
            return self.count_books

        return self.books.count()
    get_count_books.short_description = _('Count books')
    get_count_books.admin_order_field = 'count_books'


class Reply(TimeStampedModel):
    """
    Model for reply about other objects.
    """

    MAX_MARK = 5
    MIN_MARK = 1

    ERROR_MSG_UNIQUE_USER_AND_OBJECT = _('Distinct user may has alone reply')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name=_('user'),
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name=_('book'),
    )
    text_reply = models.CharField(
        _('text of reply'),
        validators=[MinLengthValidator(100)],
        max_length=1000,
        help_text=_('From 10 to 100 words.'),
    )
    advantages = ArrayField(
        models.CharField(max_length=20, validators=[OnlyLettersValidator]),
        size=10,
        verbose_name=_('advantages'),
        help_text=_('Listing from 1 to 10 words separated commas.'),
        error_messages={
            'blank': 'Enter at least one word.',
            'item_invalid': 'Word is not correct.',
        }
    )
    disadvantages = ArrayField(
        models.CharField(max_length=20, validators=[OnlyLettersValidator]),
        help_text=_('Listing from 1 to 10 words separated commas.'),
        verbose_name=_('disadvantages'),
        size=10,
        error_messages={
            'blank': 'Enter at least one word.',
            'item_invalid': 'Word is not correct.',
        }
    )
    mark_for_content = models.PositiveSmallIntegerField(
        _('mark for content'),
        default=MIN_MARK,
        validators=[
            MaxValueValidator(
                MAX_MARK, _('The mark for content must be from 1 to {}'.format(MAX_MARK))
            )
        ])
    mark_for_style = models.PositiveSmallIntegerField(
        _('mark for style'),
        default=MIN_MARK,
        validators=[
            MaxValueValidator(
                MAX_MARK, _('The mark for style must be from 1 to {}'.format(MAX_MARK))
            )
        ])
    mark_for_language = models.PositiveSmallIntegerField(
        _('mark for language'),
        default=MIN_MARK,
        validators=[
            MaxValueValidator(
                MAX_MARK, _('The mark for language must be from 1 to {}'.format(MAX_MARK))
            )
        ])

    objects = models.Manager()
    # objects = ReplyQuerySet.as_manager()

    class Meta:
        verbose_name = _('reply')
        verbose_name_plural = _('replies')
        get_latest_by = 'created'
        ordering = ('created', )
        unique_together = (('user', 'book'), )

    def __str__(self):

        return _('{0.text_reply}').format(self)

    def save(self, *args, **kwargs):

        # each word must saved as capitalize
        self.disadvantages = tuple(word.capitalize() for word in self.disadvantages)
        self.advantages = tuple(word.capitalize() for word in self.advantages)

        super(Reply, self).save(*args, **kwargs)

    def is_new(self):
        return self.created > timezone.now() - timezone.timedelta(days=settings.COUNT_DAYS_FOR_NEW_ELEMENTS)
    is_new.admin_order_field = 'created'
    is_new.short_description = _('Is new?')
    is_new.boolean = True

    def get_total_mark(self):
        """ """

        if hasattr(self, 'total_mark'):
            return self.total_mark

        total_mark = statistics.mean(
            [self.mark_for_content, self.mark_for_language, self.mark_for_style]
        )

        return round(total_mark, 3)
    get_total_mark.admin_order_field = 'total_mark'
    get_total_mark.short_description = _('Total mark')
