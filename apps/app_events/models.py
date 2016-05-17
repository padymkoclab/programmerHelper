
import uuid

# from django.template.defaultfilters import truncatewords
# from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from model_utils import Choices

# from .managers import LogQuerySet


class Event(models.Model):
    """

    """

    CHOICES_FLAGS = Choices(
        ('profiling', _('Working with profile')),
        ('adding', _('Adding')),
        ('updating', _('Updating')),
        ('deleting', _('Deleting')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='events',
        verbose_name=_('Account'),
        on_delete=models.CASCADE,
    )
    flag = models.CharField(_('Flag'), max_length=50, choices=CHOICES_FLAGS)
    message = models.TextField(_('Message'))
    date_action = models.DateTimeField(_('Date action'), auto_now_add=True)

    class Meta:
        db_table = 'events'
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        get_latest_by = 'date_action'
        ordering = ['-date_action']

    objects = models.Manager()
    # objects = LogQuerySet.as_manager()

    def __str__(self):
        return '{0.message}'.format(self)
