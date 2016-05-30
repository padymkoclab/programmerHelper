
from django.utils import timezone


class LastSeenAccountMiddleware(object):
    """
    Middleware for trake down time last seen on website.
    """

    def process_response(self, request, response):
        if request.user.is_authenticated() and response.status_code == 200:
            request.session['last_seen'] = timezone.now()
        return response
