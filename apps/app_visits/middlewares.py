
import re
from django.utils.encoding import uri_to_iri
from django.utils import timezone
from django.conf import settings


class LastSeenAccountMiddleware(object):
    """
    Middleware for trake down time last seen on website.
    """

    def process_response(self, request, response):
        if request.user.is_authenticated() and response.status_code == 200:
            request.session['last_seen'] = timezone.now()
        return response


class CountVisitsPagesMiddleware(object):
    """

    """

    SETTING_NAME_FOR_IGNORABLE_URLS = 'IGNORABLE_URLS_FOR_COUNT_VISITS'
    SESSION_VARIABLE_FOR_KEEPING_VISITED_PAGES = 'visited_pages'
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
            visited_pages = request.session.get(self.SESSION_VARIABLE_FOR_KEEPING_VISITED_PAGES, list())
            # adding new url
            visited_pages.append(url_path)
            # save new value in current session
            request.session[self.SESSION_VARIABLE_FOR_KEEPING_VISITED_PAGES] = list(set(visited_pages))
        return response


class RegistratorVisitAccountMiddleware(object):
    """

    """

    def process_response(self, request, response):
        if request.user.is_authenticated() and response.status_code == 200:
            dates_visits = request.session.get('dates_visits', list())
            if timezone.now().date() in dates_visits:
                return response
            dates_visits.append(timezone.now().date())
            request.session['dates_visits'] = list(set(dates_visits))
        return response
