
import string

from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from django.core.exceptions import ValidationError


def UserNameValidator(username):
    if len(username) < 8:
        raise ValidationError(_('Length name of account must be least 8 chars.'))
    if not all(char in string.ascii_lowercase + string.digits for char in username):
        raise ValidationError(_('Name of account must be contains only latin chars in lowercase and digits.'))
    if all(char in string.digits for char in username):
        raise ValidationError(_('Name of account can\'t be entirely numeric.'))


@deconstructible
class MaxCountWordsValidator(object):
    compare = lambda self, a, b: a > b
    # message = _('You may can using not more %(max_count_words)s words.')
    message = ungettext_lazy(
        'You may can using not more %(max_count_words)s words. Now it has %(count_words)d word.',
        'You may can using not more %(max_count_words)s words. Now it has %(count_words)d words.',
        'max_count_words')
    code = 'max_count_words'

    def __init__(self, max_count_words, message=None):
        self.max_count_words = max_count_words
        if message:
            self.message = message

    def __call__(self, text):
        count_words = self._get_count_words(text)
        params = {'max_count_words': self.max_count_words, 'count_words': count_words, 'text': text}
        if self.compare(count_words, self.max_count_words):
            raise ValidationError(self.message, code=self.code, params=params)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            (self.max_count_words == other.max_count_words) and
            (self.message == other.message) and
            (self.code == other.code)
        )

    def _get_count_words(self, text):
        return len(tuple(chars.strip() for chars in text.split(' ')))
