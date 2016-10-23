
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


def site_created(requset):
    """Added new context variable 'SITE_CREATED' on wide-website space and as dictionary."""

    try:
        SITE_CREATED = settings.SITE_CREATED
    except AttributeError:
        raise ImproperlyConfigured('Not found a setting "SITE_CREATED". Disable this middleware or create the setting.')
    return {
        'SITE_CREATED': SITE_CREATED,
    }
