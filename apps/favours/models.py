
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from mylabour.models import BaseGenericModel


class Favour(BaseGenericModel):

    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favours',
        verbose_name=_('User'),
    )
    is_favour = models.BooleanField(_('Is favour?'))
    date_modified = models.DateTimeField(_('Date last changed'), auto_now=True)

    class Meta:
        db_table = 'favours'
        verbose_name = _('Favour')
        verbose_name_plural = _('Favours')
        unique_together = ['account', 'object_id']
        get_latest_by = 'date_modified'
        ordering = ['date_modified']

    def __str__(self):
        return _('Favour on {0} "{1}"').format(
            self.content_type.model_class()._meta.verbose_name.lower(),
            self.content_object.__str__()
        )

    def clean(self):
        if self.content_object:
            if self.content_object.account == self.account:
                raise ValidationError(_('Author can`t give his favour about hisself labour.'))
