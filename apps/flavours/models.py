
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.models import BaseGenericModel


class Flavour(BaseGenericModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='flavours', verbose_name=_('User'),
    )
    status = models.BooleanField(_('Are you like it?'), default=False)

    class Meta:
        verbose_name = _('Flavour')
        verbose_name_plural = _('Flavours')
        unique_together = ['user', 'object_id']
        get_latest_by = 'date_modified'
        ordering = ['date_modified']

    def __str__(self):
        return _('On {0} "{1}"').format(
            self.content_type.model_class()._meta.verbose_name.lower(),
            self.content_object.__str__()
        )

    def clean(self):
        if self.content_object:
            if self.content_object.user == self.user:
                raise ValidationError(_('Author can`t give his flavour about hisself labour.'))
