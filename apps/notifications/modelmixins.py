
from django.utils.translation import ugettext_lazy as _


class UserNotificationModelMixin(object):
    """
    """

    def get_total_count_notifications(self):
        """Count notification send to this user."""

        if hasattr(self, 'total_count_notifications'):
            return self.total_count_notifications

        return self.notifications.count()
    get_total_count_notifications.short_description = _('Total count notifications')
    get_total_count_notifications.admin_order_field = 'total_count_notifications'

    def get_count_unread_notifications(self):
        """Count notification send to this user."""

        if hasattr(self, 'count_unread_notifications'):
            return self.count_unread_notifications

        return self.notifications.filter(is_read=False).count()
    get_count_unread_notifications.short_description = _('Count unread notifications')
    get_count_unread_notifications.admin_order_field = 'count_unread_notifications'

    def get_count_read_notifications(self):
        """Count notification send to this user."""

        if hasattr(self, 'count_read_notifications'):
            return self.count_read_notifications

        return self.notifications.filter(is_read=True).count()
    get_count_read_notifications.short_description = _('Count read notifications')
    get_count_read_notifications.admin_order_field = 'count_read_notifications'

    def get_count_deleted_notifications(self):
        """Count notification send to this user."""

        if hasattr(self, 'count_deleted_notifications'):
            return self.count_deleted_notifications

        return self.notifications.filter(is_deleted=True).count()
    get_count_deleted_notifications.short_description = _('Count deleted notifications')
    get_count_deleted_notifications.admin_order_field = 'count_deleted_notifications'
