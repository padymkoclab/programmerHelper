
import string

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


def Validator_UserName(account_name):
    if len(account_name) < 8:
        raise ValidationError(_('Length name of account must be least 8 chars.'))
    if not all(char in string.ascii_lowercase + string.digits for char in account_name):
        raise ValidationError(_('Name of account must be contains only latin chars in lowercase and digits.'))
    if all(char in string.digits for char in account_name):
        raise ValidationError(_('Name of account can\'t be entirely numeric.'))
