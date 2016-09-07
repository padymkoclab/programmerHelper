
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.models import BaseGenericModel


class Mark(BaseGenericModel):
    """
    Model for keeping mark of other objects.
    """

    MIN_MARK = 1
    MAX_MARK = 5

    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='marks',
        verbose_name=_('User'),
    )
    mark = models.SmallIntegerField(
        _('Mark'),
        default=MIN_MARK,
        validators=[MinValueValidator(MIN_MARK), MaxValueValidator(MAX_MARK)]
    )

    class Meta:
        db_table = 'marks'
        verbose_name = _('Mark')
        verbose_name_plural = _('Marks')
        permissions = (('can_view_marks', _('Can view marks')),)
        unique_together = ['account', 'object_id']
        get_latest_by = 'date_modified'
        ordering = ['date_modified']

    def __str__(self):
        type_instance = self.content_type._meta.verbose_name.lower()
        return _('Mark on {0} "{1.content_object}" from {1.account}').format(type_instance, self)

    def clean(self):
        if hasattr(self.content_object, 'account'):
            if self.content_object.account == self.account:
                raise ValidationError(_('User not allowed give mark about hisself labour.'))

    def is_new(self):
        return self.date_modified > timezone.now() - timezone.timedelta(days=settings.COUNT_DAYS_DISTINGUISH_ELEMENTS_AS_NEW)
    is_new.admin_order_field = 'date_modified'
    is_new.short_description = _('Is new?')
    is_new.boolean = True
