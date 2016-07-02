
from django.utils.translation import ugettext_lazy as _

from .models import Poll


def make_opened(modeladmin, request, queryset):
    """Admin action making selected polls as opened."""

    queryset.update(status=Poll.CHOICES_STATUS.opened)
make_opened.short_description = _('Mark selected polls as opened')


def make_draft(modeladmin, request, queryset):
    """Admin action making selected polls as draft."""

    queryset.update(status=Poll.CHOICES_STATUS.draft)
make_draft.short_description = _('Mark selected polls as draft')


def make_closed(modeladmin, request, queryset):
    """Admin action making selected polls as closed."""

    count_updated_rows = queryset.update(status=Poll.CHOICES_STATUS.closed)
    if count_updated_rows == 1:
        sub_msg = '1 poll was'
    else:
        sub_msg = '{0} polls were'.format(count_updated_rows)
    msg = '{0} succefully updated'.format(sub_msg)
    modeladmin.message_user(request, msg)
make_closed.short_description = _('Mark selected polls as closed')
