
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.models import TimeStampedModel
from utils.django.models_utils import get_admin_url


class Diary(TimeStampedModel):
    """ """

    MAX_COUNT_PARTITION = 50

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name=_('User'), related_name='diary'
    )

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

    def get_count_partitions(self):
        """ """

        if hasattr(self, 'count_partitions'):
            return self.count_partitions

        return self.partitions.count()


class Partition(TimeStampedModel):
    """ """

    diary = models.ForeignKey(
        'Diary', on_delete=models.CASCADE,
        verbose_name=_('Diary'), related_name='partitions',
    )
    name = models.CharField(_('Name'), max_length=50, unique=True)
    content = models.TextField(_('Content'))

    class Meta:
        verbose_name = _('Partition')
        verbose_name_plural = _('Partitions')
        ordering = ('diary', )
        unique_together = (('diary', 'name'), )

    def __str__(self):
        return '0.name'.format()
