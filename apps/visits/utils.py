
from .models import VisitUserSystem, VisitUserBrowser


def save_user_agent(request):

    user_agent = request.META['HTTP_USER_AGENT']

    os_name, browser_name = parse_user_agent_string(user_agent)

    update_user_pks(VisitUserSystem, os_name, request.user)
    update_user_pks(VisitUserBrowser, browser_name, request.user)


def parse_user_agent_string(user_agent_string):
    """

    """

    start_index = user_agent_string.find('(')
    end_index = user_agent_string.find(')')

    base_info = user_agent_string[:start_index]
    os_info = user_agent_string[start_index + 1:end_index]
    rest_info = user_agent_string[end_index + 1:]

    if 'Windows' in os_info:
        os_name = 'Windows'
    elif 'Macintosh' in os_info:
        os_name = 'Macintosh'
    elif 'Linux' in os_info or 'Ubuntu' in os_info or 'Debian' in os_info:
        os_name = 'Linux'

    if 'Opera' in base_info:
        browser_name = 'Opera'
    elif 'Edge' in rest_info:
        browser_name = 'Edge'
    elif 'Chrome' in rest_info and 'Safari' in rest_info:
        browser_name = 'Chrome'
    elif 'Safari' in rest_info:
        browser_name = 'Safari'
    elif 'Opera' in rest_info and 'Firefox' in rest_info:
        browser_name = 'Opera'
    elif 'Firefox' in rest_info:
        browser_name = 'Firefox'
    elif 'MSIE' in os_info or 'Trident' in os_info:
        browser_name = 'Internet Explover'

    return os_name, browser_name


def update_user_pks(model, obj_name, user):

    obj = model._default_manager.get_or_create(name=obj_name)[0]

    user_pks = obj.user_pks.split(',')
    user_pk = str(user.pk)

    if user_pk not in user_pks:

        if user_pks == ['']:
            user_pks = user_pk
        else:
            user_pks.append(user_pk)
            user_pks = ','.join(user_pks)
        obj.user_pks = user_pks
        obj.full_clean()
        obj.save()
