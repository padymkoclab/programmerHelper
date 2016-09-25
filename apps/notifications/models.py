
import uuid

from django.contrib.postgres.fields import HStoreField
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings


class Notification(models.Model):
    """ """

    NEW_MESSAGE = 'NEW_MESSAGE'
    NEW_COMMENT = 'NEW_COMMENT'
    NEW_ATTAINMENT = 'NEW_ATTAINMENT'
    LOSS_ATTAINMENT = 'LOSS_ATTAINMENT'
    CHANGING_REPUTATION = 'CHANGING_REPUTATION'
    CREATED_OBJECT = 'CREATED_OBJECT'
    UPDATED_OBJECT = 'UPDATED_OBJECT'
    DELETED_OBJECT = 'DELETED_OBJECT'
    CREATED_USER = 'CREATED_USER'
    UPDATED_USER = 'UPDATED_USER'
    UPDATED_PROFILE = 'UPDATED_PROFILE'
    UPDATED_DIARY = 'UPDATED_DIARY'
    DELETED_USER = 'DELETED_USER'

    CHOICES_ACTIONS = (
        (NEW_MESSAGE, _('New message')),
        (NEW_COMMENT, _('New comment')),
        (NEW_ATTAINMENT, _('New attainment')),
        (LOSS_ATTAINMENT, _('Loss attainment')),
        (CHANGING_REPUTATION, _('Changing reputation')),
        (CREATED_OBJECT, _('Created object')),
        (UPDATED_OBJECT, _('Updated object')),
        (DELETED_OBJECT, _('Deleted object')),
        (CREATED_USER, _('Created user')),
        (UPDATED_USER, _('Updated user')),
        (UPDATED_PROFILE, _('Updated profile')),
        (UPDATED_DIARY, _('Updated diary')),
        (DELETED_USER, _('Deleted user')),
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='notifications',
        verbose_name=_('User'), on_delete=models.CASCADE
    )
    is_read = models.BooleanField(_('Is read'), default=False, editable=False)
    content = models.CharField(_('Content'), max_length=1000)
    action = models.CharField(_('Action'), max_length=50, choices=CHOICES_ACTIONS)
    created = models.DateTimeField(_('Created'), auto_now_add=True)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        get_latest_by = 'created'
        ordering = ('-created', )

    def __str__(self):
        return self.get_action_display()

    @property
    def message(self):
        return self.determination_message()

    def send_message(self):
        pass

    def check_up_badges(self):
        pass

    def checkup_reputation(self):
        pass
