
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


def NotEndingPointValidator(value):
    if value.endswith('.'):
        raise ValidationError(_('Don`t use point in end name of category of solution.'))
