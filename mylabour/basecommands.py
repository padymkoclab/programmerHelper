
import argparse

from django.core.management import call_command
from django.core.management.base import BaseCommand


class ExtendedBaseCommand(BaseCommand):
    """Subclass from BaseCommand with extended functionality. Additional checker input and ..."""

    def __init__(self, *args, **kwargs):
        super(ExtendedBaseCommand, self).__init__(*args, **kwargs)
        self.call_command = call_command

    def _positive_integer_from_1_to_999(self, value):
        """Check up argument."""

        value = int(value)
        if value not in range(1, 1000, 1):
            msg = 'Count must be integer in range from 1 to 999 (passed %d)'
            raise argparse.ArgumentTypeError(msg % value)
        return value
