
from django.utils.html import format_html_join

from ..python.logging_utils import create_logger_by_filename
from ..python.utils import check_method_of_object

logger = create_logger_by_filename(__name__)


def listing_objects_with_admin_url(queryset, method_get_admin_url, method_get_str_obj, default_text):
    """ """

    logger.warning('If raised AttributeError or ValueError, Django replace value on empty in the Admin.')
    # details there
    # https://github.com/django/django/blob/master/django/contrib/admin/helpers.py
    # line 201

    if not queryset.exists():
        return default_text

    obj = queryset.first()
    check_method_of_object(obj, method_get_admin_url)
    check_method_of_object(obj, method_get_str_obj)

    return format_html_join(
        ', ',
        '<a href="{}">{}</a>',
        (
            (getattr(obj, method_get_admin_url)(), getattr(obj, method_get_str_obj)())
            for obj in queryset
        ),
    )


def remove_url_from_admin_urls(urls, url_name):

    acceptable_urls = (
        'changelist',
        'add',
        'history',
        'delete',
        'change',
    )

    if url_name not in acceptable_urls:
        msg = 'Not acceptable the Django`s standart admin url name ({0})'.format(
            ', '.join(acceptable_urls)
        )
        raise ValueError(msg)

    for admin_url in urls:
        if admin_url.name is not None and admin_url.name.endswith(url_name):
            urls.remove(admin_url)
