
import logging
import json

from django.core.exceptions import ImproperlyConfigured
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class InvalidTemplateVariable(str):
    """
    Class for override output that the Django template system
    determinated as invalid (e.g. misspelled) variables.
    """

    # styles for display message in HTML`s pages
    styles = mark_safe('style="color: red; font-weight: bold;"')

    def __mod__(self, variable):
        """Overide a standart output here."""

        # access to current settings
        from django.conf import settings

        # display the message on page in make log it only on stage development
        if settings.DEBUG is True:

            # format message with captured variable
            msg = 'Attention! A variable "{}" does not exists.'.format(variable)

            # get logger and make
            logger = self.get_logger()
            logger.warning(msg)

            # mark text as non-escaped in HTML
            return format_html('<i {}>{}</i>', self.styles, msg)

        # on production it will be not displayed
        return ''

    def get_logger(self):
        """Create own logger with advanced error`s details."""

        logger = logging.getLogger(self.__class__.__name__)

        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        handler.setFormatter(formatter)

        logger.addHandler(handler)

        return logger


def get_setting_from_file(setting_name, filename='secrets.json'):
    """Getting secrets settings for website from JSON-file."""

    try:
        with open(filename, 'r') as f:
            secrets_in_json = json.loads(f.read())
        return secrets_in_json[setting_name]
    except FileNotFoundError:
        raise FileNotFoundError('File "{0}" not found'.format(filename))
    except KeyError:
        message = 'Failed configured value for {0}'.format(setting_name.upper())
        raise ImproperlyConfigured(message)
