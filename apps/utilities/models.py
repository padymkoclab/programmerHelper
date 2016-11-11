
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.models import TimeStampedModel
from utils.django.models_fields import ConfiguredAutoSlugField
from utils.django.models_utils import get_admin_url

from apps.comments.models import Comment
from apps.comments.managers import CommentManager
from apps.comments.modelmixins import CommentModelMixin
from apps.opinions.models import Opinion
from apps.opinions.managers import OpinionManager
from apps.opinions.modelmixins import OpinionModelMixin

from .managers import CategoryManager, UtilityManager


class Category(TimeStampedModel):
    """
    Model of a category of utilities.
    """

    name = models.CharField(
        _('name'), max_length=100, unique=True,
        validators=[MinLengthValidator(10)],
        error_messages={
            'unique': _('Category with this name already exists.'),
        }
    )
    slug = ConfiguredAutoSlugField(populate_from='name', unique=True)
    description = models.CharField(
        _('description'), max_length=500,
        validators=[MinLengthValidator(50)]
    )

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        get_latest_by = 'date_modified'
        ordering = ['name']

    objects = models.Manager()
    objects = CategoryManager()

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('utilities:category', kwargs={'slug': self.slug})

    def get_admin_url(self):
        return get_admin_url(self)

    def get_total_mark(self):
        """ """

        if hasattr(self, 'total_mark'):
            return self.total_mark

        return self.utilities.utilities_with_marks().aggregate(
            total_mark=models.Sum('mark')
        )['total_mark'] or 0
    get_total_mark.short_description = _('Total mark')
    get_total_mark.admin_order_field = 'total_mark'

    def get_total_count_opinions(self):

        if hasattr(self, 'total_count_opinions'):
            return self.total_count_opinions

        utilities_with_count_opinions = self.utilities.utilities_with_count_opinions()
        return utilities_with_count_opinions.aggregate(
            total_count_opinions=models.Sum('count_opinions')
        )['total_count_opinions'] or 0
    get_total_count_opinions.short_description = _('Total count opinions')
    get_total_count_opinions.admin_order_field = 'total_count_opinions'

    def get_total_count_comments(self):

        if hasattr(self, 'total_count_comments'):
            return self.total_count_comments

        # create new field count_comments
        utilities_with_count_comments = self.utilities.utilities_with_count_comments()
        return utilities_with_count_comments.aggregate(
            total_count_comments=models.Sum('count_comments')
        )['total_count_comments'] or 0
    get_total_count_comments.short_description = _('Total count comments')
    get_total_count_comments.admin_order_field = 'total_count_comments'

    def get_count_utilities(self):

        if hasattr(self, 'count_utilities'):
            return self.count_utilities

        return self.utilities.prefetch_related('utilities').count()
    get_count_utilities.short_description = _('Count utilities')
    get_count_utilities.admin_order_field = 'count_utilities'


class Utility(CommentModelMixin, OpinionModelMixin, TimeStampedModel):
    """
    Model of a utility
    """

    category = models.ForeignKey(
        'Category',
        related_name='utilities',
        verbose_name=_('category'),
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        _('name'), max_length=200,
        validators=[MinLengthValidator(10)]
    )

    # As Django package manager for Tornado an Flask
    # Operating system
    # avaible language version
    # type (Package, web framework, library, service)
    # purpose
    # written on (package, programm, application, site)
    # development status
    # lisence

    description = models.TextField(_('description'), validators=[MinLengthValidator(50)])
    count_views = models.PositiveIntegerField(_('count views'), default=0, editable=False)
    web_link = models.URLField(_('web link'))

    opinions = GenericRelation(Opinion)
    comments = GenericRelation(Comment)

    class Meta:
        verbose_name = _("utility")
        verbose_name_plural = _("utilities")
        ordering = ('category', 'name')
        unique_together = (('category', 'name'), )

    objects = models.Manager()
    objects = UtilityManager()

    comments_manager = CommentManager()
    opinions_manager = OpinionManager()

    def __str__(self):
        return '{0.name}'.format(self)

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('category', 'name'):
            return _('Utility with this name already exists in this category')
        return super().unique_error_message(model_class, unique_check)
