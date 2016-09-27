
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def admin_staff_member_required(
    view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
    login_url='admin:login', cacheable=False
):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, redirecting to the login page if necessary.

    Also it make csrf_protect for each view and if need mark as chachable
    """

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    view_func = actual_decorator(view_func)

    # make views as non chached
    if not cacheable:
        view_func = never_cache(view_func)

    # We add csrf_protect here so this function can be used as a utility
    # function for any view, without having to repeat 'csrf_protect'.
    if not getattr(view_func, 'csrf_exempt', False):
        view_func = csrf_protect(view_func)

    return view_func
