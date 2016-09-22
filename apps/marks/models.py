
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

    user = models.ForeignKey(
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
        unique_together = ['user', 'object_id']
        get_latest_by = 'date_modified'
        ordering = ['date_modified']

    def __str__(self):
        return _('On {0} "{1.content_object}"').format(
            self.content_object._meta.verbose_name.lower(),
            self
        )

    def clean(self):
        if hasattr(self.content_object, 'user'):
            if self.content_object.user == self.user:
                raise ValidationError(_('User not allowed give mark about hisself labour.'))

    def is_new(self):
        return self.date_modified > timezone.now() - timezone.timedelta(days=settings.COUNT_DAYS_FOR_NEW_ELEMENTS)
    is_new.admin_order_field = 'date_modified'
    is_new.short_description = _('Is new?')
    is_new.boolean = True
