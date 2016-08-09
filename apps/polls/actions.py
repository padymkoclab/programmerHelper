
from django.utils.translation import ugettext_lazy
from django.utils.translation import ungettext_lazy

from .models import Poll


def make_update_queryset_and_return_msg_to_user(modeladmin, request, queryset, status):
    """Make update a queryset by passed status and
    return message about count updated polls."""

    # a method update() does not with annotation of queryset by models.Count()
    # so, make repeated sample objects by their primary keys

    count_updated_rows = Poll.objects.filter(pk__in=queryset).update(status=status)
    msg = ungettext_lazy(
        '%(num)d poll was succefully updated',
        '%(num)d polls was succefully updated',
        'num') % {'num': count_updated_rows}
    return msg


def make_opened(modeladmin, request, queryset):
    """Admin action making selected polls as opened."""

    make_update_queryset_and_return_msg_to_user(modeladmin, request, queryset, 'opened')
make_opened.short_description = ugettext_lazy('Mark selected polls as opened')


def make_draft(modeladmin, request, queryset):
    """Admin action making selected polls as draft."""

    make_update_queryset_and_return_msg_to_user(modeladmin, request, queryset, 'draft')
make_draft.short_description = ugettext_lazy('Mark selected polls as draft')


def make_closed(modeladmin, request, queryset):
    """Admin action making selected polls as closed."""

    make_update_queryset_and_return_msg_to_user(modeladmin, request, queryset, 'closed')
make_closed.short_description = ugettext_lazy('Mark selected polls as closed')
