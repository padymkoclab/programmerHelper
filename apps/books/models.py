
import statistics
import itertools
import collections
import uuid

from psycopg2.extras import NumericRange
from django.contrib.postgres.fields import IntegerRangeField
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from mylabour.fields_db import ConfiguredAutoSlugField
from apps.replies.models import Reply
from apps.tags.models import Tag

from .managers import BookManager, WritterManager
from .querysets import BookQuerySet, WritterQuerySet


NOW_YEAR = timezone.datetime.now().year

# announs book, soon
#
# read with Scrapy data from Amazon.com


class Book(models.Model):
    """
    Model for books
    """

    # display language name on Site Language for user

    LANGUAGES = tuple((code, _(name)) for code, name in settings.LANGUAGES)

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(
        _('Name'),
        max_length=200,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)],
        unique=True,
    )
    slug = ConfiguredAutoSlugField(_('Slug'), populate_from='name', unique=True)
    description = models.TextField(
        _('Description'),
        validators=[MinLengthValidator(100)],
        help_text=_('Minimal length 100 characters.'),
    )
    picture = models.URLField(_('Picture'), max_length=1000)
    language = models.CharField(_('Language'), max_length=25, choices=LANGUAGES)
    pages = models.PositiveSmallIntegerField(_('Count pages'), validators=[MinValueValidator(1)])
    accounts = models.ManyToManyField(
        'Writter',
        verbose_name=_('Authorship'),
        related_name='books',
    )
    publishers = models.CharField(_('Publishers'), max_length=100, blank=True, default='')
    isbn = models.CharField(
        _('ISBN'),
        max_length=30,
        help_text=_('ISBN code of book'),
        validators=[RegexValidator(regex='\d+-\d+-\d+-\d+-\d+')],
        blank=True,
        default='',
    )
    year_published = models.PositiveSmallIntegerField(
        _('Year published'),
        validators=[
            MinValueValidator(1950, _('Book doesn`t possible will published early than 1950.')),
            MaxValueValidator(NOW_YEAR, _('Book doesn`t possible will published in future.')),
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
        ordering = ['year_published', 'name']

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('books:book', kwargs={'slug': self.slug})

    def get_admin_page_url(self):
        return reverse(
            'admin:{0}_{1}_change'.format(self._meta.app_label, self._meta.model_name),
            args=(self.pk,)
        )

    def get_rating(self):
        """Getting rating of book on based scopes."""

        # return self.__class__.objects.books_with_rating().get(pk=self.pk).rating
        replies_with_total_scope = self.replies.replies_with_total_scope()
        rating = replies_with_total_scope.aggregate(rating=models.Avg('total_scope'))['rating']
        rating = rating or 0
        return round(rating, 4)
    get_rating.admin_order_field = 'rating'
    get_rating.short_description = _('Rating')

    def is_new(self):
        """This book published in this year or one year ago."""

        return self in self.__class__.objects.new_books()
    is_new.admin_order_field = 'year_published'
    is_new.short_description = _('Is new')
    is_new.boolean = True

    def get_size(self):
        """Getting size of books on based count pages."""

        return self.__class__.objects.books_with_sizes().get(pk=self.pk).size
    get_size.admin_order_field = 'pages'
    get_size.short_description = _('Size')

    # Whar often tell about this book
    # Display return words by font size: h1 h2 h3 and so.
    def most_common_words_from_replies(self):
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


class Writter(models.Model):
    """
    Model for writters of books
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(
        _('Name'),
        max_length=200,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)],
        unique=True,
        error_messages={'unique': _('The such writter already is here.')}
    )
    slug = ConfiguredAutoSlugField(_('Slug'), populate_from='name', unique=True)
    #
    # basic trends of books
    #
    about = models.TextField(
        _('About writter'),
        validators=[MinLengthValidator(100)],
        help_text=_('Give brief character of the writter and his books.')
    )
    years_life = IntegerRangeField(
        _('years life'),
        null=True,
        blank=True,
        help_text='Enter year birth and year death, if aware.'
    )

    class Meta:
        db_table = 'writters'
        verbose_name = _('Writter')
        verbose_name_plural = _('Writters')
        ordering = ['name']

    objects = models.Manager()
    objects = WritterManager.from_queryset(WritterQuerySet)()

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('books:writter', kwargs={'slug': self.slug})

    def clean(self):
        if self.years_life is not None:
            if not isinstance(self.years_life, NumericRange):
                raise ValidationError(
                    {'years_life': _('Years life of writter must be passed as not empty sequence with two values.')}
                )

            # accept only None or integer
            year_birth = self.years_life.lower
            year_death = self.years_life.upper
            if not (type(year_birth) == int or year_birth is None) or \
                    not (type(year_death) == int or year_death is None):
                raise ValidationError(
                    {'years_life': _('Year birth and death must be integer or skiped.')}
                )

            #
            if year_birth is not None:
                if not 1000 <= year_birth <= NOW_YEAR - 20:
                    raise ValidationError(
                        {'years_life': _('Writter may can bithed only from 1000 A. D. to {0} year.').format(NOW_YEAR - 20)}
                    )
            if year_death is not None:
                if not 1000 <= year_death <= NOW_YEAR:
                    raise ValidationError(
                        {'years_life': _('Writter may can dead only from 1000 A. D. to now year.')}
                    )
            if year_death is not None and year_birth is not None:
                if year_birth >= year_death:
                    raise ValidationError({
                        'years_life': [_('Year of birth can not more or equal year of dearth.')]
                    })
                elif self.get_age() < 20:
                    raise ValidationError({
                        'years_life': [_('Very small range between year of birth and year of death.')]
                    })
                elif self.get_age() > 100:
                    raise ValidationError({
                        'years_life': [
                            _('Very big range between year of birth and year of death ({0} years).').format(self.get_age())
                        ]
                    })

    def get_age(self):
        """Getting age writter if it is possible."""

        try:
            age = self.years_life.upper - self.years_life.lower
            assert age > 0
            return age
        except:
            return None

    def show_years_life(self):
        """Show age`s writter in human view."""

        birth_year = self.years_life.lower
        death_year = self.years_life.upper

        # chage value None on ????
        if birth_year is None:
            birth_year = '????'
        if death_year is None:
            death_year = '????'

        return '{0} - {1}'.format(birth_year, death_year)
    show_years_life.short_description = _('Year life')

    def get_avg_scope_for_books(self):
        """Getting avarage scope for books`s writter, on based average rating it books."""

        all_scopes_books = tuple((book.get_rating() for book in self.books.iterator()))
        if all_scopes_books:
            return round(statistics.mean(all_scopes_books), 4)
        return 0.0
