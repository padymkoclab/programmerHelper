
# from django.contrib.auth import get_user_model

from apps.app_sessions.models import ExtendedSession


def count_visits(request):
    count_visits_this_page = 1
    for session in ExtendedSession.objects.iterator():
        visited_pages = session.get_decoded().get('visited_pages', [])
        if request.path_info in visited_pages:
            count_visits_this_page += 1
    context = {'count_visits_this_page': count_visits_this_page}
    return context
