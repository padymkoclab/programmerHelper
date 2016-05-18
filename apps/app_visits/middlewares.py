
from django.utils import timezone


class LastSeenAccountMiddleware(object):

    def process_response(self, request, response):
        if request.user.is_authenticated():
            request.session['last_seen'] = timezone.now()
        return response


class CountVisitsMiddleware(object):

    def process_response(self, request, response):
        if request.user.is_authenticated():
            url_path = request.get_full_path()
            request.session[url_path] = True
        return response
