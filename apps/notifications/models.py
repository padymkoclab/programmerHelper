
import uuid

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.datetime_utils import convert_date_to_django_date_format

from .managers import NotificationManager


class Notification(models.Model):
    """ """

    SUCCESS = 'success'
    INFO = 'info'
    ERROR = 'error'
    WARNING = 'warning'

    CHOICES_LEVEL = (
        (SUCCESS, _('Success')),
        (INFO, _('Info')),
        (ERROR, _('Error')),
        (WARNING, _('Warning')),
    )

    is_real_object = None

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    level = models.CharField(_('level'), default=INFO, choices=CHOICES_LEVEL, max_length=10)
    action = models.CharField(_('action'), max_length=200)

    is_read = models.BooleanField(_('is read?'), default=False)
    is_deleted = models.BooleanField(_('is deleted?'), default=False)
    is_public = models.BooleanField(_('is public?'), default=True)
    is_emailed = models.BooleanField(_('is emailed?'), default=True)

    created = models.DateTimeField(_('created'), auto_now_add=True)

    # recipient = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, related_name='notifications',
    #     verbose_name=_('recipient'), on_delete=models.CASCADE
    # )

    actor_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        related_name='notifications_actors',
    )
    actor_object_id = models.CharField(max_length=200, null=True, blank=True)
    actor = GenericForeignKey(ct_field='actor_content_type', fk_field='actor_object_id')

    target_content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='notifications_targets',
    )
    target_object_id = models.CharField(max_length=200, null=True, blank=True)
    target = GenericForeignKey(ct_field='target_content_type', fk_field='target_object_id')

    objects = models.Manager()
    objects = NotificationManager()

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        get_latest_by = 'created'
        ordering = ('-created', )

    def __str__(self):
        return self.get_short_message()

    def save(self, *args, **kwargs):

        if self.is_real_object is None:
            self.is_real_object = False if self.target is None else True

        super(Notification, self).save(*args, **kwargs)

    def get_full_message(self):
        pass

    def get_short_message(self):

        created = convert_date_to_django_date_format(self.created)

        if self.actor is None and self.target is None:
            return 'Anybody made {} on {}'.format(
                self.action,
                created,
            )

        elif self.target is None:

            return '{} "{}" {} "(deleted object)" on {}'.format(
                self.actor._meta.verbose_name,
                self.actor,
                self.action,
                created,
            )

        elif self.actor is None:

            return 'Anybody made {} {} "{}" on {}'.format(
                self.action,
                self.target._meta.verbose_name.lower(),
                self.target,
                created,
            )

        return '{} "{}" {} {} "{}" on {}'.format(
            self.actor._meta.verbose_name,
            self.actor,
            self.action,
            self.target._meta.verbose_name.lower(),
            self.target,
            created,
        )

    def mark_as_read(self):
        pass

    def mark_as_unread(self):
        pass

    def mark_as_deleted(self):
        pass

    def mark_as_undeleted(self):
        pass


class Follow(models.Model):
    """

    """

    models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    11
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        related_name='follow', db_index=True
    )
    object_id = models.TextField(db_index=True)
    content_object = GenericForeignKey(
        ct_field='content_type', fk_field='object_id'
    )
    started = models.DateTimeField(_('started'))

    class Meta:
        verbose_name = "Follow"
        verbose_name_plural = "Follows"
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self):

        return '{0.user} --> {0.content_object}'.format(self)
