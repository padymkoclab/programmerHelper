
import re
import datetime

from django.utils.encoding import uri_to_iri
from django.conf import settings

from .models import Visit, DayAttendance


class RegistratorVisitAccountMiddleware(object):
    """
    Registrator dates visits of website the users.
    """

    def process_response(self, request, response):
        if request.user.is_authenticated() and response.status_code == 200:
            DayAttendance.objects.get_or_create(user=request.user, day_attendance=datetime.date.today())
        return response


class CountVisitsPagesMiddleware(object):
    """
    Count visits pages by authenticated users.
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
        if request.user.is_authenticated() and response.status_code == 200:
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
