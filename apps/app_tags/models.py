
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models

from mylabour.models import TimeStampedModel

from .managers import TagQuerySet, TagManager


class Tag(TimeStampedModel):
    """
    Model tags for another models
    """

    MIN_COUNT_TAGS_ON_OBJECT = 1
    MAX_COUNT_TAGS_ON_OBJECT = 5

    name = models.SlugField(_('Name'), max_length=30, unique=True, allow_unicode=True)

    class Meta:
        db_table = 'tags'
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        get_latest_by = 'date_modified'
        ordering = ['name']

    # managers
    objects = models.Manager()
    objects = TagManager.from_queryset(TagQuerySet)()

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('app_tags:tag', kwargs={'slug': self.name})

    def count_usage(self):
        pass
