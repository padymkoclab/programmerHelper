
import statistics
import itertools
import collections
import uuid

from django.contrib.postgres.fields import ArrayField
from django.utils.html import format_html
from django.db.models.functions import Coalesce
from utils.django.functions_db import Round
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.models_fields import ConfiguredAutoSlugField, CountryField
from utils.python.logging_utils import create_logger_by_filename

from apps.replies.models import Reply
from apps.tags.models import Tag

from .managers import BookManager, WriterManager
from .querysets import BookQuerySet, WriterQuerySet, PublisherQuerySet


# announs book, soon
#
# read with Scrapy data from Amazon.com


logger = create_logger_by_filename(__name__)
NOW_YEAR = timezone.now().year


class Book(models.Model):
    """
    Model for books
    """

    MIN_YEAR_PUBLISHED = 1950
    MAX_YEAR_PUBLISHED = NOW_YEAR

    LANGUAGES = tuple((code, _(name)) for code, name in settings.LANGUAGES)

    # display language name on Site Language for user

    def upload_book_image(instance, filename):
        return 'books/{slug}/{filename}'.format(slug=instance.slug, filename=filename)

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(
        _('Name'),
        max_length=100,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)],
        unique=True,
    )
    slug = ConfiguredAutoSlugField(_('Slug'), populate_from='name', unique=True)
    description = models.TextField(
        _('Description'),
        validators=[MinLengthValidator(100)],
        help_text=_('Minimal length 100 characters.'),
    )
    image = models.ImageField(_('Image'), upload_to=upload_book_image, max_length=1000)
    language = models.CharField(_('Language'), max_length=25, choices=LANGUAGES, default='en')
    count_pages = models.PositiveSmallIntegerField(_('Count pages'), validators=[MinValueValidator(1)])
    authorship = models.ManyToManyField(
        'Writer',
        verbose_name=_('Authorship'),
        related_name='books',
    )
    publisher = models.ForeignKey('Publisher', verbose_name=_('Publisher'), related_name='books')
    isbn = models.CharField(
        _('ISBN'),
        max_length=30,
        help_text=_('ISBN code of a book'),
        validators=[
            RegexValidator(
                regex='\d+-\d+-\d+-\d+-\d+',
                message=_('Not correct ISBN for a book'),
            )
        ],
        blank=True,
        default='',
    )
    year_published = models.PositiveSmallIntegerField(
        _('Year published'),
        validators=[
            MinValueValidator(
                MIN_YEAR_PUBLISHED,
                _('Book doesn`t possible will published early than {0}.'.format(MIN_YEAR_PUBLISHED))
            ),
            MaxValueValidator(
                MAX_YEAR_PUBLISHED,
                _('Book doesn`t possible will published in future.')
            ),
        ]
    )
    date_added = models.DateTimeField(_('Date added'), auto_now_add=True)
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('Tags'),
        related_name='books',
    )
    replies = GenericRelation(Reply, related_query_name='books')

    # managers
    objects = models.Manager()
    objects = BookManager.from_queryset(BookQuerySet)()

    class Meta:
        db_table = 'books'
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        get_latest_by = 'year_published'
        ordering = ['date_added']

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('books:book', kwargs={'slug': self.slug})

    def get_admin_url(self):
        return reverse(
            'admin:{0}_{1}_change'.format(self._meta.app_label, self._meta.model_name),
            args=(self.pk,)
        )

    def get_count_tags(self):
        return self.tags.count()
    get_count_tags.admin_order_field = 'count_tags'
    get_count_tags.short_description = _('Count tags')

    def get_count_replies(self):
        return self.replies.count()
    get_count_replies.admin_order_field = 'count_replies'
    get_count_replies.short_description = _('Count replies')

    def get_rating(self):
        """Getting rating of book on based marks."""

        if self.replies.exists():
            replies_with_total_mark = self.replies.replies_with_total_mark()
            rating = replies_with_total_mark.aggregate(rating=models.Avg('total_mark'))['rating']
            return round(rating, 3)
        return
    get_rating.admin_order_field = 'rating'
    get_rating.short_description = _('Rating')

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
    get_size_display.admin_order_field = 'pages'
    get_size_display.short_description = _('Size')

    def get_image_thumbnail(self):
        return format_html('<image src={0} />', self.image.url)
    get_image_thumbnail.short_description = _('Picture')

    # Whar often tell about this book
    # Display return words by font size: h1 h2 h3 and so.
    def get_most_common_words_from_replies(self):
        """Determining most common words presents in replies."""

        # get all words in advantages and disadvantages of reply as two-nested list
        all_words_in_two_nested_list_words = self.replies.values_list('advantages', 'disadvantages')

        # flat two-nested list to single list
        two_nested_list_words = itertools.chain.from_iterable(all_words_in_two_nested_list_words)
        single_nested_list_words = itertools.chain.from_iterable(two_nested_list_words)

        # exceute count words
        counter_words = collections.Counter(single_nested_list_words)

        # return 10 most common words
        return counter_words.most_common(10)


class Writer(models.Model):
    """
    Model for writers of books
    """

    MIN_BIRTH_YEAR = 1900
    MAX_BIRTH_YEAR = NOW_YEAR - 16
    MIN_DEATH_YEAR = 1916
    MAX_DEATH_YEAR = NOW_YEAR

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(
        _('Name'),
        max_length=200,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)],
        unique=True,
        error_messages={'unique': _('Writer with this name already exists.')}
    )
    slug = ConfiguredAutoSlugField(_('Slug'), populate_from='name', unique=True)
    trends = ArrayField(
        models.CharField(max_length=100),
        size=10,
        help_text=_('Basic trends of books. Make listing words separated commas.')
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
            MaxValueValidator(MAX_DEATH_YEAR, 'Writer not possible dead in future')
        ],
    )

    class Meta:
        db_table = 'writers'
        verbose_name = _('Writer')
        verbose_name_plural = _('Writers')
        ordering = ['name']

    objects = models.Manager()
    objects = WriterManager.from_queryset(WriterQuerySet)()

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
        return self.books.count()
    get_count_books.admin_order_field = 'count_books'
    get_count_books.short_description = _('Count books')

    def get_age(self):
        """Getting age writer if it is possible."""

        if self.death_year is None:
            return self.MAX_DEATH_YEAR - self.birth_year
        return self.death_year - self.birth_year
    get_age.short_description = _('Age')
    get_age.admin_order_field = 'age'

    def get_years_life(self):
        """Return years of life of writer, replace 0 on sign '?'."""

        return '{0} - {1}'.format(self.birth_year, '' if self.death_year is None else self.death_year)
    get_years_life.short_description = _('Year life')

    def is_alive_writer(self):
        """Return boolean - this writer now is living?"""

        if self.death_year is None:
            return True
        return False
    is_alive_writer.short_description = _('Is alive?')
    is_alive_writer.admin_order_field = 'is_alive'
    is_alive_writer.boolean = True

    def get_avg_mark_for_books(self):
        """Getting avarage mark for books`s writer, on based average rating it books."""

        logger.debug('Rewrite SQL for books_with_rating()')
        # books = self.books.books_with_rating()
        # return books.aggregate(rating_avg=Coalesce(Round(models.Avg('rating')), Value(0.0)))['rating_avg']

        if self.books.exists():
            avg_mark_for_books = statistics.mean(book.get_rating() or 0 for book in self.books.iterator())
            avg_mark_for_books = round(avg_mark_for_books, 3)
            return avg_mark_for_books
        return
    get_avg_mark_for_books.short_description = _('Average mark for books')
    # get_avg_mark_for_books.admin_order_field


class Publisher(models.Model):

    MIN_FOUNDED_YEAR = 1900
    MAX_FOUNDED_YEAR = NOW_YEAR

    name = models.CharField(
        _('name'), max_length=50, unique=True,
        error_messages={'unique': _('Publisher with this name already exists.')}
    )
    slug = ConfiguredAutoSlugField(_('slug'), populate_from='name', unique=True)
    country_origin = CountryField()
    headquarters = models.CharField(_('headquarters'), max_length=50)
    founded_year = models.PositiveSmallIntegerField(
        _('Founded year'),
        validators=[
            MinValueValidator(
                MIN_FOUNDED_YEAR,
                _('Publishing company not possible founded early than {}'.format(MIN_FOUNDED_YEAR))
            ),
            MaxValueValidator(MAX_FOUNDED_YEAR, _('Publishing company not possible founded in future')),
        ])
    website = models.URLField(_('Official website'))

    objects = models.Manager()
    objects = PublisherQuerySet.as_manager()

    class Meta:
        db_table = 'publisher'
        verbose_name = _('Publisher')
        verbose_name_plural = _('Publishers')
        ordering = ['name']

    def __str__(self):
        return '{0}'.format(self.name)

    def get_absolute_url(self):
        return reverse('books:publisher', kwargs={'slug': self.slug})

    def get_admin_url(self):
        return reverse('admin:books_publisher_change', args=(self.pk, ))

    def get_count_books(self):
        return self.books.count()
    get_count_books.short_description = _('Count books')
    get_count_books.admin_order_field = 'count_books'
