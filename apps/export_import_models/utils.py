
from django.utils import timezone


def get_filename_by_datetime_name_and_extension(name, extension):
    """Return filename with determined name, current datetime in internation format and extension."""

    now = timezone.now()

    # truncated version datetime ISO format (withput microseconds and and timezone)
    datetime_ISO_format = now.strftime('%Y-%m-%d_%H:%M:%S')

    return '{0}_{1}.{2}'.format(name, datetime_ISO_format, extension)
