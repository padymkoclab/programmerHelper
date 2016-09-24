
from django.conf import settings
from django.contrib.auth import get_user_model
from importlib import import_module

from .models import Visit


User = get_user_model()
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


def count_visits(request):
    count_visits_this_page = Visit.objects.get_count_visits_by_url(url=request.path_info)
    context = {'count_visits_this_page': count_visits_this_page}
    return context


def users_online(request):
    """ """

    users_online = list()

    SessionStoreModel = SessionStore().model

    for session in SessionStoreModel._default_manager.iterator():
        user_pk = session.get_decoded()['_auth_user_id']

        user = User._default_manager.get(pk__exact=user_pk)
        users_online.append(user)

    return {'users_online': users_online}
