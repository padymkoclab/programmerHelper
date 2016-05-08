
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField

from apps.app_generic_models.models import UserOpinion_Generic, UserComment_Generic
from mylabour.models import TimeStampedModel


# Are you agree?

class ProgrammingCategory(TimeStampedModel):
    """

    """

    name = models.CharField(
        _('Name'), max_length=200, unique=True, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True, db_index=True, allow_unicode=True)
    description = models.TextField(_('Description'))
    picture = models.URLField(_('Picture'), max_length=1000)
    views = models.IntegerField(_('Count views'), default=0, editable=False)

    class Meta:
        db_table = 'programming_categories'
        verbose_name = _("Programming category")
        verbose_name_plural = _("Programming categories")
        get_latest_by = 'date_modified'
        ordering = ['name']

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('app_programming_utilities:programming_category', kwargs={'slug': self.slug})

# show comments (default hide)


class ProgrammingUtility(TimeStampedModel):
    """

    """

    name = models.CharField(
        _('Name'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    description = models.TextField(_('Description'))
    picture = models.URLField(_('Picture'), max_length=1000)
    category = models.ForeignKey(
        'ProgrammingCategory',
        related_name='programming_utilities',
        verbose_name=_('Category'),
        on_delete=models.CASCADE,
    )
    web_link = models.URLField(_('Web link'))
    opinions = GenericRelation(UserOpinion_Generic)
    comments = GenericRelation(UserComment_Generic)

    class Meta:
        db_table = 'programming_utilities'
        verbose_name = _("Utility")
        verbose_name_plural = _("Utilities")
        ordering = ['category', 'name']
        unique_together = ['name', 'category']

    def __str__(self):
        return '{0.name}'.format(self)
