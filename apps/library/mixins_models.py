
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserReplyModelMixin(object):
    """

    """

    def get_date_latest_reply(self):
        """ """

        if hasattr(self, 'date_latest_reply'):
            return self.date_latest_reply

        return self.replies.aggregate(date_latest_reply=models.Max('created'))['date_latest_reply']
    get_date_latest_reply.admin_order_field = 'date_latest_reply'
    get_date_latest_reply.short_description = _('Latest reply')

    def get_count_replies(self):
        """ """

        if hasattr(self, 'count_replies'):
            return self.count_replies

        return self.replies.count()
    get_count_replies.admin_order_field = 'count_replies'
    get_count_replies.short_description = _('Count replies')

    def get_book_with_latest_reply_and_admin_url(self):

        latest_reply = self.replies.order_by('-created').first()
        return None if latest_reply is None else latest_reply.book
    get_book_with_latest_reply_and_admin_url.short_description = _('Book with latest replies')
    get_book_with_latest_reply_and_admin_url.with_change_admin_url = True
