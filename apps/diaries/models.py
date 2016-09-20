
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.models import TimeStampedModel


#
# What are you technologies using?
# What you will read?
# What you read already?


class Diary(TimeStampedModel):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name=_('User'), related_name='diary'
    )

    class Meta:
        verbose_name = _('Diary')
        verbose_name_plural = _('Diaries')
        ordering = ('user', )

    def __str__(self):
        return ('Diary of user {0.user}').format(self)

    def get_absolute_url(self):
        return reverse('')

    @property
    def date_created(self):
        return self.user.date_joined
