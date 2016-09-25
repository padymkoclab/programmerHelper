
import string

from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from utils.python.constants import RUSSIAN_LETTERS


@deconstructible
class UsernameValidator:

    acceptable_characters = string.ascii_letters + string.digits + '+-_' + RUSSIAN_LETTERS
    help_text = _('Username may contains digits, ascii and russian letters, signs \'+\', \'-\', \'_\'')
    code = 'invalid_username'

    def __call__(self, value):

        if not all(i in self.acceptable_characters for i in value):
            raise ValidationError('Username contains non acceptable characters')
