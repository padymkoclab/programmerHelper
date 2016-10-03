
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.models import TimeStampedModel
from utils.django.models_fields import ConfiguredAutoSlugField
from utils.django.models_utils import get_admin_url, upload_image

from apps.comments.models import Comment
from apps.comments.managers import CommentManager
from apps.comments.models_mixins import CommentsModelMixin
from apps.opinions.models import Opinion
from apps.opinions.managers import OpinionManager
from apps.opinions.models_mixins import OpinionsModelMixin
# from apps.flavours.models import Flavour
# from apps.flavours.managers import FlavourManager
# from apps.flavours.models_mixins import FlavourModelMixin

from .querysets import UtilityQuerySet, CategoryQuerySet
from .managers import CategoryManager, UtilityManager


class Category(TimeStampedModel):
    """
    Model of a category of utilities.
    """

    name = models.CharField(
        _('Name'), max_length=100, unique=True,
        validators=[MinLengthValidator(10)],
        error_messages={
            'unique': _('Category with this name already exists.'),
        }
    )
    slug = ConfiguredAutoSlugField(populate_from='name', unique=True)
    description = models.CharField(
        _('Description'), max_length=500,
        validators=[MinLengthValidator(50)]
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        get_latest_by = 'date_modified'
        ordering = ['name']

    objects = models.Manager()
    objects = CategoryManager.from_queryset(CategoryQuerySet)()

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


class Utility(CommentsModelMixin, OpinionsModelMixin, TimeStampedModel):
    """
    Model of a utility
    """

    name = models.CharField(
        _('Name'), max_length=200,
        validators=[MinLengthValidator(10)]
    )
    description = models.TextField(_('Description'), validators=[MinLengthValidator(50)])
    category = models.ForeignKey(
        'Category',
        related_name='utilities',
        verbose_name=_('Category'),
        on_delete=models.CASCADE,
    )
    web_link = models.URLField(_('Web link'))

    opinions = GenericRelation(Opinion)
    comments = GenericRelation(Comment)

    class Meta:
        verbose_name = _("Utility")
        verbose_name_plural = _("Utilities")
        ordering = ['category', 'name']
        unique_together = ['category', 'name']

    objects = models.Manager()
    objects = UtilityManager.from_queryset(UtilityQuerySet)()

    comments_manager = CommentManager()
    opinions_manager = OpinionManager()

    def __str__(self):
        return '{0.name}'.format(self)
