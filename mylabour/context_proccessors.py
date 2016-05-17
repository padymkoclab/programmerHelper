
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils import timezone
from django.core.exceptions import ImproperlyConfigure
from django.conf import settings


def time_existence_of_website(requset):
    """Added new context variable 'time_existence_of_website' on wide-website space and as dictionary."""

    # trying getting setting DATE_CREATING_WEBSITE
    try:
        date_creating_website = settings.DATE_CREATING_WEBSITE
    except AttributeError:
        raise ImproperlyConfigure('Not found setting DATE_CREATING_WEBSITE.')
    # checkup not correct value setting DATE_CREATING_WEBSITE
    now = timezone.now()
    if now > DATE_CREATING_WEBSITE:
        raise ValueError('Date creating website is in future.')
    # getting time existence of website in human-readable form
    time_existence_of_website = naturaltime(date_creating_website)
    return {'time_existence_of_website': time_existence_of_website}
