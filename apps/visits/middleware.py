
import re

from django.utils import timezone
from django.conf import settings
from django.core.cache import cache
from django.utils.encoding import uri_to_iri

from .models import Visit, VisitSite, VisitPage
from .constants import AUTHENTICATED_USERS_KEY, ANONYMOUS_USERS_KEY


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
    BOTS_USER_AGENT = [
        "Teoma", "alexa", "froogle", "Gigabot", "inktomi", "looksmart", "URL_Spider_SQL", "Firefly",
        "NationalDirectory", "Ask Jeeves", "TECNOSEEK", "InfoSeek", "WebFindBot", "girafabot", "crawler",
        "www.galaxy.com", "Googlebot", "Googlebot/2.1", "Google", "Webmaster", "Scooter", "James Bond",
        "Slurp", "msnbot", "appie", "FAST", "WebBug", "Spade", "ZyBorg", "rabaz", "Baiduspider",
        "Feedfetcher-Google", "TechnoratiSnoop", "Rankivabot", "Mediapartners-Google", "Sogou web spider",
        "WebAlta Crawler", "MJ12bot", "Yandex/", "YaDirectBot", "StackRambler", "DotBot", "dotbot"
    ]

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if response.status_code == 200:

            VisitPage.objects.change_url_counter(request)

        return response

    def _is_ignorable_URL(self, url_path, list_igno_urls):
        return any(re.search(pattern, url_path) for pattern in list_igno_urls)

    def _check_present_setting_for_restriction_urls_for_count(self):
        try:
            list_igno_urls = getattr(settings, self.SETTING_NAME_FOR_IGNORABLE_URLS)
        except AttributeError:
            Warning(
                """
                You don\'t have settings for restinction ignorable urls.
                Therefore will be not restinction for adding new urls.
                """)
            return False
        else:
            return list_igno_urls if list_igno_urls else False

    def process_response(self, request, response):
        if response.status_code == 200:
            if request.user.is_authenticated():
                # correct displaying unicode in URL
                url_path = uri_to_iri(request.path)
                # check_url_as_ignorabled if defined corresponding setting
                list_igno_urls = self._check_present_setting_for_restriction_urls_for_count()
                if list_igno_urls:
                    if self._is_ignorable_URL(url_path, list_igno_urls):
                        return response
                # get value variable stored in session or create new as list()
                visit = Visit.objects.get_or_create(url__exact=url_path)[0]
                visit.users.add(request.user)
        return response


class UsersOnlineMiddleware:
    """
    Determinate online users: registered and anonimus
    """

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        authenticated_users = cache.get(AUTHENTICATED_USERS_KEY, set())
        anonymous_users = cache.get(ANONYMOUS_USERS_KEY, set())

        if request.user.is_authenticated():
            authenticated_users.add(request.user)

        else:
            session_id = request.COOKIES.get(settings.SESSION_COOKIE_NAME, '')
            anonymous_users.add(session_id)

        cache.set(AUTHENTICATED_USERS_KEY, authenticated_users, settings.CHECK_USERS_ONLINE_TIMEOUT)
        cache.set(ANONYMOUS_USERS_KEY, anonymous_users, settings.CHECK_USERS_ONLINE_TIMEOUT)

        response = self.get_response(request)

        if response.status_code == 200:
            pass

        return response
