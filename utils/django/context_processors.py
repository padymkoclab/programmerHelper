
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


def date_creating_website(requset):
    """Added new context variable 'DATE_CREATING_WEBSITE' on wide-website space and as dictionary."""

    # trying getting setting DATE_CREATING_WEBSITE
    try:
        date_creating_website = settings.DATE_CREATING_SITE
    except AttributeError:
        raise ImproperlyConfigured('Not found setting DATE_CREATING_WEBSITE.')
    return {'date_creating_website': date_creating_website}
