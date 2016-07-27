
import argparse

from django.core.management.base import BaseCommand


class ExtendedBaseCommand(BaseCommand):
    """Subclass from BaseCommand with extended functionality. Additional checker input and ..."""

    def _positive_integer_from_1_to_999(self, value):
        """Check up argument."""

        value = int(value)
        if value not in range(1, 1000, 1):
            msg = '%d is an invalid positive integer in range from 1 to 999'
            raise argparse.ArgumentTypeError(msg % value)
        return value
