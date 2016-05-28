
import uuid

from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


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


class BaseGenericModel(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('Type object'))
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
