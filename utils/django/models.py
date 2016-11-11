
import uuid

from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Timestampable(models.Model):
    """
    Abstract base models with two fields: created and updated. And too supported localization.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updated = models.DateTimeField(_('date modified'), auto_now=True)
    created = models.DateTimeField(_('date added'), auto_now_add=True)

    class Meta:
        abstract = True

    def is_new(self):
        return self.created > \
            timezone.now() - timezone.timedelta(
                days=settings.COUNT_DAYS_FOR_NEW_ELEMENTS
            )
    is_new.admin_order_field = 'created'
    is_new.short_description = _('is new?')
    is_new.boolean = True


class GenericRelatable(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('type object'))
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class Moderatable(models.Model):
    """

    """

    approved = models.BooleanField(_('approved'), default=False)

    class Meta:
        abstract = True


class Orderable(models.Model):
    """

    """

    position = models.PositiveSmallIntegerField(_('position'))

    class Meta:
        abstract = True


class Scheduleable(models.Model):
    """

    """

    started = models.DateTimeField(_('started'))
    ended = models.DateTimeField(_('ended'))

    class Meta:
        abstract = True


class Permalinkable(models.Model):
    """

    """

    position = models.SlugField(_('slug'))

    class Meta:
        abstract = True


class Userable(models.Model):
    """

    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name=_('user'))

    class Meta:
        abstract = True


class Publishable(models.Model):
    """

    """

    PUBLISHED = 'published'
    DRAFT = 'draft'
    STATUS_CHOICES = (
        (PUBLISHED, _('Published')),
        (DRAFT, _('Draft')),
    )

    status = models.CharField(_('status'), choices=STATUS_CHOICES, max_length=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name=_('user'))

    class Meta:
        abstract = True


class Viewable(models.Model):
    """

    """

    count_views = models.PositiveIntegerField(_('count views'), default=0)

    class Meta:
        abstract = True
