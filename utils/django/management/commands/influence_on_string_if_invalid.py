
from django.utils.safestring import mark_safe
from django.conf import settings

from ...basecommands import ExtendedBaseCommand
from ....python.logging_utils import create_logger_by_filename

logger = create_logger_by_filename(__name__)


raise NotImplementedError(
    'Problem is there https://docs.djangoproject.com/en/1.8/topics/settings/#altering-settings-at-runtime'
)


class Command(ExtendedBaseCommand):

    help = 'Change values string_if_invalid in settings'

    def add_arguments(self, parser):
        parser.add_argument('status', choices=['on', 'off'])

    def handle(self, *args, **kwargs):

        status = kwargs['status']

        if status == 'on':
            value = mark_safe('<i style="color: red; font-weight: bold;">Variable does not exists!!!</i>')
        elif status == 'off':
            value = None

        settings.TEMPLATES[0]['OPTIONS']['string_if_invalid'] = value

        settings._wrapped.INSTALLED_APPS = ()

        settings.DEBUG = False

        logger.info('Changed value in settings: string_if_invalid now is {}'.format(status))
