
import uuid

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from utils.python.utils import classproperty
from utils.django.datetime_utils import convert_date_to_django_date_format

from .managers import NotificationManager
from .constants import Action


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

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    level = models.CharField(_('level'), default=SUCCESS, choices=CHOICES_LEVEL, max_length=10)
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

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('user'),
        related_name='+', on_delete=models.SET_NULL, null=True, blank=True
    )
    user_display_text = models.CharField(_('user_display_text'), max_length=100, blank=True)

    target_content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='notifications_targets',
    )
    target_object_id = models.CharField(max_length=200, null=True, blank=True)
    target = GenericForeignKey(ct_field='target_content_type', fk_field='target_object_id')
    target_str = models.CharField(_('target'), max_length=200, null=True, blank=True)

    action_target_content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='notifications_action_targets',
    )
    action_target_object_id = models.CharField(max_length=200, null=True, blank=True)
    action_target = GenericForeignKey(ct_field='action_target_content_type', fk_field='action_target_object_id')

    objects = models.Manager()
    objects = NotificationManager()

    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        get_latest_by = 'created'
        ordering = ('-created', )

    def __str__(self):

        action = self.get_action_display()
        user_display_text = self.get_user_display_text()
        created = convert_date_to_django_date_format(self.created)

        if self.has_target():

            target_content_type_name, target_display_text = self.get_target_info()

            return '{} "{}" {} {} "{}" on {}'.format(
                self.user_verbose_name,
                user_display_text,
                action,
                self.target_type_verbose_name,
                self.target_str,
                created,
            )

        return '{} "{}" {} on {}'.format(
            self.user_verbose_name, user_display_text, action, created
        )

    def save(self, *args, **kwargs):

        target = kwargs.pop('target', None)
        if target is not None:
            self.target_str = str(target)
            self.full_clean()

        user = kwargs.pop('user', None)
        if user is not None:
            self.user_display_text = user.get_full_name()
            self.full_clean()

        super(Notification, self).save(*args, **kwargs)

    def mark_as_read(self):

        if self.is_read is False:
            self.is_read = True
            self.full_clean()
            self.save()

    def mark_as_unread(self):

        if self.is_read is True:
            self.is_read = False
            self.full_clean()
            self.save()

    def mark_as_deleted(self):

        if self.is_deleted is False:
            self.is_deleted = True
            self.full_clean()
            self.save()

    def mark_as_undeleted(self):

        if self.is_deleted is True:
            self.is_deleted = False
            self.full_clean()
            self.save()

    def get_target_info(self):

        if self.target is None:
            target_content_type_name = self.target_content_type.model_class()._meta.verbose_name.lower()
            target_display_text = self.target_str
        else:
            target_content_type_name = self.target._meta.verbose_name.lower()
            target_display_text = str(self.target)

        return target_content_type_name, target_display_text

    def get_user_display_text(self):

        if self.user is None:
            return self.user_display_text
        return self.user.get_full_name()

    @classproperty
    def user_verbose_name(self):

        return get_user_model()._meta.verbose_name

    def has_target(self):

        return self.target is not None or self.target_content_type is not None

    @property
    def target_type_verbose_name(self):

        if self.has_target():

            target_model = self.target_content_type.model_class()
            return target_model._meta.verbose_name

        return self.user_verbose_name

    @property
    def action_target_type_verbose_name(self):

        if self.action_target_content_type is not None:

            action_target_model = self.action_target_content_type.model_class()
            return action_target_model._meta.verbose_name

        return self.target_type_verbose_name

    def get_action_display(self):

        return Action.get_action_display(self.action)

    def get_type_action_title(self):

        return Action.get_type_action_title(self.action)


class Follow(models.Model):
    """

    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

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
