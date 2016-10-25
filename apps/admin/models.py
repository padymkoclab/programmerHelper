
import json
import logging
import uuid

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings


class LogEntry(models.Model):

    ADDED = 1
    CHANGED = 2
    DELETED = 3

    CHOISES_ACTION = (
        (ADDED, _('Added')),
        (CHANGED, _('Changed')),
        (DELETED, _('Deleted')),
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    action_time = models.DateTimeField(
        _('time of action'),
        auto_now_add=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('user'),
        on_delete=models.CASCADE, related_name='admin_actions',
    )
    content_type = models.ForeignKey(
        ContentType, models.SET_NULL, null=True,
        verbose_name=_('content type'), blank=True,
    )
    object_id = models.TextField(_('object ID'))
    action = models.PositiveIntegerField(_('Action'), choices=CHOISES_ACTION)

    objects = models.Manager()

    class Meta:
        db_table = 'admin_admin_log_entries'
        verbose_name = "log entry"
        verbose_name_plural = "log entries"
        ordering = ('-action_time', )

    def __str__(self):

        return 'LogEntry object'

    def get_admin_url_object(self):
        return ('')

    def get_message(self):
        pass

    def is_added(self):

        return self.action == self.ADDED

    def is_changed(self):

        return self.action == self.CHANGED

    def is_deleted(self):

        return self.action == self.DELETED
