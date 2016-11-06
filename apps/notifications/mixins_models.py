
from django.utils.translation import ugettext_lazy as _


class UserNotificationModelMixin(object):
    """

    """

    def get_notifications(self, by_type='all'):

        if by_type not in ['all', 'read', 'unread']:
            raise ValueError('')

        return self.notifications.order_by('-created')

    def get_total_count_notifications(self):
        """Count notification send to this user."""

        raise NotImplementedError
    get_total_count_notifications.short_description = _('Total count notifications')
    get_total_count_notifications.admin_order_field = 'total_count_notifications'

    def get_count_unread_notifications(self):
        """Count notification send to this user."""

        raise NotImplementedError
    get_count_unread_notifications.short_description = _('Count unread notifications')
    get_count_unread_notifications.admin_order_field = 'count_unread_notifications'

    def get_count_read_notifications(self):
        """Count notification send to this user."""

        raise NotImplementedError
    get_count_read_notifications.short_description = _('Count read notifications')
    get_count_read_notifications.admin_order_field = 'count_read_notifications'
