
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models

from autoslug import AutoSlugField

from mylabour.models import TimeStampedModel


class Tag(TimeStampedModel):
    """
    Model tags for another models
    """

    name = models.CharField(_('Name'), max_length=30, unique=True)
    slug = AutoSlugField(_('Slug'), populate_from='name', unique=True, always_update=True, allow_unicode=True)

    class Meta:
        db_table = 'tags'
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        get_latest_by = 'date_modified'
        ordering = ['name']

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('app_tags:tag', kwargs={'slug': self.slug})
