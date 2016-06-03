
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField

from mylabour.models import TimeStampedModel


class Newsletter(TimeStampedModel):

    title = models.CharField(
        _('Title'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(populate_from='title', unique_with=['account'], always_update=True)
    content = models.TextField(_('Content'), validators=[MinLengthValidator(100, _('Minimum 100 characters.'))])
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='news',
        verbose_name=_('Author'),
        limit_choices_to={'is_active': True},
    )
    web_link = models.URLField(_('Web link'))

    class Meta:
        db_table = 'newsletters'
        verbose_name = _("Newsletter")
        verbose_name_plural = _("Newsletters")
        get_latest_by = 'date_added'
        ordering = ['date_added']
        unique_together = ['title', 'account']

    def __str__(self):
        return '{0.title}'.format(self)

    def get_absolute_url(self):
        return reverse('newsletters:newsletter', kwargs={'slug': self.slug})
