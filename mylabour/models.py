
import uuid

from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models

from model_utils import Choices


class TimeStampedModel(models.Model):
    """
    Abstract base models with two fields: date_added and date_modified. And too supported localization.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_modified = models.DateTimeField(_('Date last changed'), auto_now=True)
    date_added = models.DateTimeField(_('Date added'), auto_now_add=True)

    class Meta:
        abstract = True

    def is_new(self):
        return self.date_added > timezone.now() - timezone.timedelta(days=settings.COUNT_DAYS_DISTINGUISH_ELEMENTS_AS_NEW)
    is_new.admin_order_field = 'date_added'
    is_new.short_description = _('Is new?')
    is_new.boolean = True


class OpinionUserModel(models.Model):
    """

    """

    CHOICES_FAVORITE = Choices(
        ('yes', _('Yes')),
        ('unknown', _('Unknown')),
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    is_useful = models.NullBooleanField(_('Is was useful for you?'))
    is_favorite = models.CharField(
        _('Is your favorite theme?'),
        max_length=30,
        choices=CHOICES_FAVORITE,
        default=CHOICES_FAVORITE.unknown,
    )
    date_modified = models.DateTimeField(_('Date modified'), auto_now=True)

    class Meta:
        abstract = True
        get_latest_by = 'date_modified'
        permissions = (('can_view_opinions', _('Can view opinions')),)

    def display_is_favorite_as_boolean(self):
        if self.is_favorite == self.CHOICES_FAVORITE.yes:
            return True
        if self.is_favorite == self.CHOICES_FAVORITE.unknown:
            return None
    display_is_favorite_as_boolean.boolean = True
    display_is_favorite_as_boolean.admin_order_field = 'is_favorite'
    display_is_favorite_as_boolean.short_description = _('Is favorite')


class LikeUserModel(models.Model):
    """

    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    liked_it = models.BooleanField(_('Liked it?'))
    date_modified = models.DateTimeField(_('Date modified'), auto_now=True)

    class Meta:
        abstract = True
        get_latest_by = 'date_modified'
        ordering = ['date_modified']
        permissions = (('can_view_opinions', _('Can view opinions')),)
