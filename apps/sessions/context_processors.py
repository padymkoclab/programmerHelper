
from django.contrib.auth import get_user_model

from .models import ExpandedSession


def users_online(request):
    """Determinete the online-users."""

    pks_online_users = ExpandedSession.objects.values_list('account_pk', flat=True)
    users_online = get_user_model().objects.only('email').filter(pk__in=pks_online_users)
    credentials_online_users = ', '.join(account.get_full_name() for account in users_online)
    return {
        'count_online_users': len(users_online),
        'credentials_online_users': credentials_online_users,
    }
