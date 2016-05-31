
import uuid

from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from mylabour.fields_db import ConfiguredAutoSlugField
from apps.scopes.models import Scope
from apps.replies.models import Reply
from apps.tags.models import Tag
from apps.web_links.models import WebLink

from .managers import BookManager
from .querysets import BookQuerySet


NOW_YEAR = timezone.datetime.now().year


# announs book, soon

class Book(models.Model):
    """
    Model for books
    """

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
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('Tags'),
        related_name='books',
    )
    links = models.ManyToManyField(
        WebLink,
        related_name='books',
        verbose_name=_('Where downloads'),
        help_text=_('Weblinks where can download this book.')
    )
    scopes = GenericRelation(Scope, related_query_name='books')
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

    def get_rating(self):
        """Getting rating of book on based scopes."""

        return self.__class__.objects.books_with_rating().get(pk=self.pk).rating
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

        pass


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
        error_messages={'unique': _('Such writter already exists.')}
    )
    slug = ConfiguredAutoSlugField(_('Slug'), populate_from='name', unique=True)
    about = models.TextField(
        _('About writter'),
        validators=[MinLengthValidator(100)],
        help_text=_('Give brief character of the writter and his books.')
    )
    birthyear = models.SmallIntegerField(
        _('Birthyear'),
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(NOW_YEAR, _('Year of birth can not in future.')),
        ])
    deathyear = models.SmallIntegerField(
        _('Deathyear'),
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(NOW_YEAR, _('Year of death can not in future.')),
        ]
    )

    class Meta:
        db_table = 'writters'
        verbose_name = _('Writter')
        verbose_name_plural = _('Writters')
        ordering = ['name']

    objects = models.Manager()

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('books:writter', kwargs={'slug': self.slug})

    def clean(self):
        if isinstance(self.birthyear, int) and isinstance(self.deathyear, int):
            if self.birthyear >= self.deathyear:
                raise ValidationError({
                    '__all__': [_('Year of birth can not more or equal year of dearth.')]
                })
            if not self.deathyear - self.birthyear > 20:
                raise ValidationError({
                    '__all__': [_('Very small range between year of birth and year of death.')]
                })
            if not self.deathyear - self.birthyear <= 150:
                raise ValidationError({
                    '__all__': [_('Very big range between year of birth and year of death.')]
                })
        if isinstance(self.birthyear, int):
            if self.birthyear > NOW_YEAR - 20:
                raise ValidationError({
                    'birthyear': [_('Writter not possible born so early.')]
                })
