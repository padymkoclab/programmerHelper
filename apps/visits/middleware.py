
import re
import logging

from django.utils import timezone
from django.conf import settings
from django.core.cache import cache
from django.utils.encoding import uri_to_iri

from .models import Visit, VisitSite, VisitPage
from .constants import AUTHENTICATED_USERS_KEY, ANONYMOUS_USERS_KEY
from .utils import save_user_agent


logger = logging.getLogger('django.development')


class UserVisitMiddleware(object):
    """
    Registrator dates visits of website the users.
    """

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if response.status_code == 200:
            if request.user.is_authenticated():

                now = timezone.now()
                today = now.date()
                if not VisitSite.objects.filter(date=today, users=request.user).exists():
                    attendance = VisitSite.objects.get_or_create(date=today)[0]
                    attendance.users.add(request.user)

                Visit.objects.get_or_create(user=request.user, defaults={'date': now})

        return response


class CounterVisitPageMiddleware(object):
    """
    Count visits pages by users. Counter will be increase even if the same user again visited page.
    """

    SETTING_NAME_FOR_IGNORABLE_URLS = 'IGNORABLE_URLS_FOR_COUNT_VISITS'

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if response.status_code == 200:

            VisitPage.objects.change_url_counter(request)

        return response

    def _is_ignorable_URL(self, url_path, list_igno_urls):
        return any(re.search(pattern, url_path) for pattern in list_igno_urls)


class UsersOnlineMiddleware:
    """
    Determinate online users: registered and anonimus
    """

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        authenticated_users = cache.get(AUTHENTICATED_USERS_KEY, dict())
        anonymous_users = cache.get(ANONYMOUS_USERS_KEY, dict())

        now = timezone.now()
        date_expiration = timezone.now() + timezone.timedelta(seconds=settings.CHECK_USERS_ONLINE_TIMEOUT)

        if request.user.is_authenticated():
            authenticated_users[request.user] = date_expiration

        else:
            session_id = request.COOKIES.get(settings.SESSION_COOKIE_NAME, '')
            anonymous_users[session_id] = date_expiration

            logger.critical('Anonymous users always not more 1')

        for obj, date_expiration in authenticated_users.copy().items():
            if date_expiration < now:
                del authenticated_users[obj]

        for obj, date_expiration in anonymous_users.copy().items():
            if date_expiration < now:
                del anonymous_users[obj]

        # 1 hour
        cache.set(AUTHENTICATED_USERS_KEY, authenticated_users, 60 * 60)
        cache.set(ANONYMOUS_USERS_KEY, anonymous_users, 60 * 60)

        response = self.get_response(request)

        if response.status_code == 200:
            pass

        return response


class UserAgentUsageMiddleware:
    """
    Determinate online users: registered and anonimus
    """

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if response.status_code == 200:
            if request.user.is_authenticated():
                save_user_agent(request)

        return response
