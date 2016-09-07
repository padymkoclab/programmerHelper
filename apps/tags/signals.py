
from django.core.management import call_command

from utils.python.logging_utils import create_logger_by_filename


logger = create_logger_by_filename(__name__)


def create_tags_if_yet_not(sender, **kwargs):
    call_command('create_tags')
    logger.debug('Signal post_migrate for app Tags was called.')
