
import statistics
import uuid

from django.utils.html import format_html_join
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField

from apps.app_generic_models.models import UserComment_Generic, UserOpinion_Generic
from apps.app_tags.models import Tag
from apps.app_web_links.models import WebLink


class Book(models.Model):
    """
    Model for books
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(
        _('Name'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(_('Slug'), populate_from='name', unique=True, always_update=True, allow_unicode=True, db_index=True)
    description = models.TextField(_('Description'))
    picture = models.URLField(_('Picture'), max_length=1000)
    pages = models.PositiveSmallIntegerField(_('Count pages'), validators=[MinValueValidator(1)])
    views = models.PositiveIntegerField(_('Count views'), default=0, editable=False)
    authorship = models.ManyToManyField(
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
    date_published = models.DateField(_('Date published'))
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('Tags'),
        related_name='books',
    )
    where_download = models.ManyToManyField(
        WebLink,
        related_name='books',
        verbose_name=_('Where downloads')
    )
    comments = GenericRelation(UserComment_Generic)
    opinions = GenericRelation(UserOpinion_Generic)

    class Meta:
        db_table = 'books'
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        get_latest_by = 'date_published'
        ordering = ['date_published', 'name']

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('app_books:book', kwargs={'slug': self.slug})

    def get_scope(self):
        # no sorted in admin
        goods = UserOpinion_Generic.objects.filter(object_id=self.pk, is_useful=True).count()
        bads = UserOpinion_Generic.objects.filter(object_id=self.pk, is_useful=False).count()
        return statistics.mean([goods, bads])
    # get_scope.admin_order_field = 'date_published'
    get_scope.short_description = _('Scope')

    def is_new(self):
        """This book pusblished about one year ago."""
        return timezone.now().date() >= self.date_published - timezone.timedelta(weeks=52)
    is_new.admin_order_field = 'date_published'
    is_new.short_description = _('Is new')
    is_new.boolean = True

    def writters(self):
        """Listing writters separated throgh commas"""
        return format_html_join(', ', '{0}', ((writter, ) for writter in self.authorship.all()))
    writters.short_description = _('Writters')


class Writter(models.Model):
    """
    Model for writters of books
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(
        _('Name'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(_('Slug'), populate_from='name', unique=True, always_update=True, allow_unicode=True, db_index=True)
    about = models.TextField(_('About writter'))

    class Meta:
        db_table = 'writters'
        verbose_name = _('Writter')
        verbose_name_plural = _('Writters')
        ordering = ['name']

    objects = models.Manager()

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('app_books:writter', kwargs={'slug': self.slug})
