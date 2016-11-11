
from django.utils.translation import ugettext_lazy as _


class UserVisitModelMixin(object):
    """
    """

    def get_last_seen(self):

        if hasattr(self, 'last_seen'):
            return self.last_seen.date
        return
    get_last_seen.short_description = _('Last seen')
    get_last_seen.admin_order_field = 'last_seen'

    def get_count_days_attendances(self):

        return self.attendances.count()
    get_count_days_attendances.short_description = _('Count days attendance')
    get_count_days_attendances.admin_order_field = 'count_days_attendance'
