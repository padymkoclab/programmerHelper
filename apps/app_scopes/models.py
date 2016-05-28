
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from mylabour.models import BaseGenericModel


class Scope(BaseGenericModel):
    """

    """

    MIN_SCOPE = 0
    MAX_SCOPE = 5

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scopes',
        verbose_name=_('User'),
    )
    scope = models.SmallIntegerField(
        _('Scope'),
        default=MIN_SCOPE,
        validators=[MinValueValidator(MIN_SCOPE), MaxValueValidator(MAX_SCOPE)]
    )
    date_modified = models.DateTimeField(_('Date last changed'))

    class Meta:
        db_table = 'scopes'
        verbose_name = _('Scope')
        verbose_name_plural = _('Scopes')
        permissions = (('can_view_scopes', _('Can view scopes')),)
        unique_together = ['user', 'object_id']
        get_latest_by = 'date_modified'
        ordering = ['date_modified']

    def clean(self):
        if self.content_object.author == self.user:
            raise ValidationError(_('User not allowed give scope about hisself labour.'))

    def save(self, *args, **kwargs):
        self.clean()
        super(Scope, self).save(*args, **kwargs)

    def is_new(self):
        return self.date_modified > timezone.now() - timezone.timedelta(days=settings.COUNT_DAYS_DISTINGUISH_ELEMENTS_AS_NEW)
    is_new.admin_order_field = 'date_modified'
    is_new.short_description = _('Is new?')
    is_new.boolean = True
