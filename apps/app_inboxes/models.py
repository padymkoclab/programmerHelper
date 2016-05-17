
import uuid

from django.template.defaultfilters import truncatewords
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings


class Inbox(models.Model):
    """

    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='inbox',
        verbose_name=_('Account'),
        on_delete=models.CASCADE,
    )
    message = models.TextField(_('Message'))
    date_received = models.DateTimeField(_('Date received'), auto_now_add=True)

    class Meta:
        db_table = 'inboxes'
        verbose_name = _('Inbox')
        verbose_name_plural = _('Inboxes')
        get_latest_by = 'date_received'
        ordering = ['date_received']

    objects = models.Manager()

    def __str__(self):
        return '{0.message}'.format(self)

    def truncated_message(self):
        return truncatewords(self.message, 10)
