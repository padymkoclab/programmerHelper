
import uuid

from django.template.defaultfilters import truncatewords
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings


class Notification(models.Model):
    """

    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='notifications',
        verbose_name=_('Account'),
        on_delete=models.CASCADE,
    )
    # title
    # reason
    # priority
    message = models.TextField(_('Message'))
    date = models.DateTimeField(_('Date received'), auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        get_latest_by = 'date'
        ordering = ['date']

    objects = models.Manager()

    def __str__(self):
        return '{0.message}'.format(self)

    def truncated_message(self):
        return truncatewords(self.message, 10)

# new model Priority
