
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from mylabour.fields_db import ConfiguredAutoSlugField
from mylabour.models import TimeStampedModel

from apps.comments.models import Comment
from apps.opinions.models import Opinion

from .querysets import UtilityQuerySet, UtilityCategoryQuerySet


# Are you agree?

class UtilityCategory(TimeStampedModel):
    """
    Model category of utilities.
    """

    def upload_category_image(instance, filename):
        return 'utilities/categories/{0}/{1}'.format(instance.slug, filename)

    name = models.CharField(
        _('Name'), max_length=100, unique=True,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = ConfiguredAutoSlugField(populate_from='name', unique=True)
    description = models.CharField(
        _('Description'), max_length=500,
        validators=[MinLengthValidator(50)]
    )
    image = models.ImageField(_('Picture'), max_length=1000, upload_to=upload_category_image)

    class Meta:
        db_table = 'utilities_categories'
        verbose_name = _("Category of utilities")
        verbose_name_plural = _("Categories of utilities")
        get_latest_by = 'date_modified'
        ordering = ['name']

    objects = models.Manager()
    objects = UtilityCategoryQuerySet.as_manager()

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('utilities:category', kwargs={'slug': self.slug})

    def get_admin_url(self):
        return reverse('admin:utilities_utilitycategory_change', args=(self.pk, ))

    def get_total_mark(self):
        return sum(utility.get_mark() for utility in self.utilities.iterator())
    get_total_mark.short_description = _('Total mark')

    def get_total_opinions(self):
        # create new field count_opinions
        annotated_utilities = self.utilities.annotate(count_opinions=models.Count('opinions'))
        # summarize aggregation on field count_opinions of utilities
        aggregate_utilities = annotated_utilities.aggregate(total_count_opinions=models.Sum('count_opinions'))
        return aggregate_utilities['total_count_opinions'] or 0
    get_total_opinions.short_description = _('Count opinions')

    def get_total_comments(self):
        # create new field count_comments
        annotated_utilities = self.utilities.annotate(count_comments=models.Count('comments'))
        # summarize aggregation on field count_comments of utilities
        aggregate_utilities = annotated_utilities.aggregate(total_count_comments=models.Sum('count_comments'))
        return aggregate_utilities['total_count_comments'] or 0
    get_total_comments.short_description = _('Count comments')

    def get_count_utilities(self):
        return self.utilities.count()


class Utility(TimeStampedModel):
    """
    Model for utility
    """

    name = models.CharField(
        _('Name'), max_length=200,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    description = models.CharField(
        _('Description'), max_length=500,
        validators=[MinLengthValidator(50)]
    )
    category = models.ForeignKey(
        'UtilityCategory',
        related_name='utilities',
        verbose_name=_('Category'),
        on_delete=models.CASCADE,
    )
    web_link = models.URLField(_('Web link'))

    opinions = GenericRelation(Opinion)
    comments = GenericRelation(Comment)

    class Meta:
        db_table = 'utilities'
        verbose_name = _("Utility")
        verbose_name_plural = _("Utilities")
        ordering = ['category', 'name']
        unique_together = ['category', 'name']

    objects = models.Manager()
    objects = UtilityQuerySet.as_manager()

    def __str__(self):
        return '{0.name}'.format(self)

    def get_mark(self):
        good_opinions = self.opinions.filter(is_useful=True).count()
        bad_opinions = self.opinions.filter(is_useful=False).count()
        return good_opinions - bad_opinions
    get_mark.short_description = _('Mark')

    def get_count_comments(self):
        return self.comments.count()

    def get_count_replies(self):
        return self.replies.count()
