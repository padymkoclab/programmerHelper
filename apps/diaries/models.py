
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.models import TimeStampedModel
from utils.django.models_utils import get_admin_url

from .managers import DiaryManager


class Diary(TimeStampedModel):
    """ """

    MAX_COUNT_PARTITION = 50

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name=_('User'), related_name='diary'
    )

    objects = models.Manager()
    objects = DiaryManager()

    class Meta:
        verbose_name = _('Diary')
        verbose_name_plural = _('Diaries')
        ordering = ('user', )

    def __str__(self):
        return '{0.user}'.format(self)

    def get_absolute_url(self):
        return 'ERROR'
        return reverse('')

    def get_admin_url(self):
        return get_admin_url(self)

    def get_date_latest_changes(self):
        """ """

        if self.partitions.exists():
            return self.partitions.latest().updated
        return

    def get_count_partitions(self):
        """ """

        if hasattr(self, 'count_partitions'):
            return self.count_partitions

        return self.partitions.count()
    get_count_partitions.admin_order_field = 'count_partitions'


class Partition(TimeStampedModel):
    """ """

    diary = models.ForeignKey(
        'Diary', on_delete=models.CASCADE,
        verbose_name=_('Diary'), related_name='partitions',
    )
    name = models.CharField(_('name'), max_length=50, unique=True)
    content = models.TextField(_('content'))

    class Meta:
        verbose_name = _('Partition')
        verbose_name_plural = _('Partitions')
        ordering = ('diary', )
        get_latest_by = 'updated'
        unique_together = (('diary', 'name'), )

    def __str__(self):
        return '{0.name}'.format(self)

    def unique_error_message(self, model_class, unique_check):

        if unique_check == ('diary', 'name'):

            return ValidationError(
                message=_("Partition with this name already exists."),
                code='unique_together',
            )
        return super().unique_error_message(model_class, unique_check)
