
import uuid

# from django.template.defaultfilters import truncatewords
# from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from .managers import ActivityManager


class Activity(models.Model):
    """

    """

    USER = 'USER'
    ADD = 'ADD'
    UPDT = 'UPDT'
    DEL = 'DEL'

    CHOICES_FLAGS = (
        (USER, _('Working with profile')),
        (ADD, _('Adding')),
        (UPDT, _('Updating')),
        (DEL, _('Deleting')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='activity',
        verbose_name=_('Account'),
        on_delete=models.CASCADE,
    )
    flag = models.CharField(_('Flag'), max_length=50, choices=CHOICES_FLAGS)
    message = models.TextField(_('Message'))
    date = models.DateTimeField(_('Date'), auto_now_add=True)

    class Meta:
        db_table = 'activity'
        verbose_name = _('Activity')
        verbose_name_plural = _('Activity')
        get_latest_by = 'date'
        ordering = ['-date']

    objects = models.Manager()
    objects = ActivityManager()

    def __str__(self):
        return '{0.message}'.format(self)
