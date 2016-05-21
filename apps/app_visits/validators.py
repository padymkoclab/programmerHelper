
import re

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


def validate_url_path(url_path):
    is_valid = re.match(r'^/[-._/\w]+$', url_path)
    if not is_valid:
        msg = _('Enter valid path of URL.')
        raise ValidationError(msg)
