
from django.utils.translation import ugettext_lazy as _


class CommentsModelMixin:

    def get_count_comments(self):
        """ """

        if hasattr(self, 'count_comments'):
            return self.count_comments

        return self.comments.count()
    get_count_comments.admin_order_field = 'count_comments'
    get_count_comments.short_description = _('Count comments')
