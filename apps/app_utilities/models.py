
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField

from apps.app_comments.models import Comment
from apps.app_opinions.models import Opinion
from mylabour.models import TimeStampedModel


# Are you agree?

class UtilityCategory(TimeStampedModel):
    """
    Category of unitilities.
    """

    name = models.CharField(
        _('Name'), max_length=200, unique=True, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True, db_index=True, allow_unicode=True)
    description = models.TextField(_('Description'))
    picture = models.URLField(_('Picture'), max_length=1000)
    views = models.IntegerField(_('Count views'), default=0, editable=False)

    class Meta:
        db_table = 'utilities_categories'
        verbose_name = _("Category of utilities")
        verbose_name_plural = _("Categories of utilities")
        get_latest_by = 'date_modified'
        ordering = ['name']

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('app_utilities:category', kwargs={'slug': self.slug})

    def get_total_scope(self):
        return sum(utility.get_scope() for utility in self.utilities.iterator())
    get_total_scope.short_description = _('Rating')

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


class Utility(TimeStampedModel):
    """

    """

    name = models.CharField(
        _('Name'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    description = models.TextField(_('Description'))
    picture = models.URLField(_('Picture'), max_length=1000)
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
        unique_together = ['name', 'category']

    def __str__(self):
        return '{0.name}'.format(self)

    def get_scope(self):
        good_opinions = self.opinions.filter(is_useful=True).count()
        bad_opinions = self.opinions.filter(is_useful=False).count()
        return good_opinions - bad_opinions
    get_scope.short_description = _('Scope')
