
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from mylabour.models import BaseGenericModel


class Opinion(BaseGenericModel):

    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='opinions',
        verbose_name=_('User'),
    )
    is_useful = models.BooleanField(_('Is useful?'))
    date_modified = models.DateTimeField(_('Date last changed'), auto_now=True)

    class Meta:
        db_table = 'opinions'
        verbose_name = _('Opinion')
        verbose_name_plural = _('Opinions')
        permissions = (('can_view_opinions', _('Can view opinions')),)
        unique_together = ['account', 'object_id']
        get_latest_by = 'date_modified'
        ordering = ['date_modified']

    def __str__(self):
        if self.content_object:
            return _('Opinion about {0} "{1}"').format(
                self.content_object._meta.verbose_name.lower(),
                self.content_object.__str__()
            )
        return str()

    def save(self, *args, **kwargs):
        super(Opinion, self).save(*args, **kwargs)

    def clean(self):
        if self.content_object:
            if self.content_object.account == self.account:
                raise ValidationError(_('Author not allowed have opinion about hisself labour.'))
