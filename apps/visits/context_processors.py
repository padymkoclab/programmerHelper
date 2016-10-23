
from importlib import import_module

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache

from .models import VisitPage
from .constants import AUTHENTICATED_USERS_KEY, ANONYMOUS_USERS_KEY


User = get_user_model()
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


def count_visits_page(request):

    count_visits_page = VisitPage.objects.get_count_visits(request)

    return {
        'COUNT_VISITS_PAGE': count_visits_page,
    }


def online_users(request):
    """ """

    online_authenticated_users = cache.get(AUTHENTICATED_USERS_KEY)
    online_anonymous_users = cache.get(ANONYMOUS_USERS_KEY)

    return {
        'ONLINE_AUTHENTICATED_USERS': online_authenticated_users,
        'ONLINE_ANONYMOUS_USERS': online_anonymous_users,
    }
