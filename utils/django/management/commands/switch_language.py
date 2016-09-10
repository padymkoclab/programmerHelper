
from django.core.management.base import BaseCommand
from django.utils.translation import get_language_info, activate
from django.conf import settings


raise NotImplementedError(
    'Problem is there https://docs.djangoproject.com/en/1.8/topics/settings/#altering-settings-at-runtime'
)


def _get_help_text():
    """Return detailed help_text for command."""

    lst_languages_info = list()
    msg = 'Switch language for whole project, from avaliable languages. Now is avaliable next languages: '

    for code, lang in settings.LANGUAGES:
        lang_info = get_language_info(code)
        lang_info_detail = '{0} ({1}) with code "{2}"'.format(
            lang_info['name_local'],
            lang_info['name'],
            lang_info['code'],
        )
        lst_languages_info.append(lang_info_detail)

    msg += ', '.join(lst_languages_info)
    return msg


class Command(BaseCommand):

    help = _get_help_text()

    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('language_code', nargs=1, type=str, choices=self._get_avaibled_languages_codes())

    def handle(self, *args, **kwargs):
        raise NotImplementedError
        language_code = kwargs['language_code'][0]
        activate(language_code)

    @staticmethod
    def _get_avaibled_languages_codes():
        return tuple(code for code, lang in settings.LANGUAGES)
