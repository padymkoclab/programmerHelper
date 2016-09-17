
import collections

from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.python.utils import flatten


class RepliesModelMixin:

    def get_count_replies(self):
        """ """

        if hasattr(self, 'count_replies'):
            return self.count_replies

        return self.replies.count()
    get_count_replies.admin_order_field = 'count_replies'
    get_count_replies.short_description = _('Count replies')

    def get_rating(self):
        """Getting rating of book on based marks."""

        if hasattr(self, 'rating'):
            return self.rating

        replies_with_total_mark = self.replies.replies_with_total_mark()
        rating = replies_with_total_mark.aggregate(rating=models.Avg('total_mark'))['rating']
        if rating is not None:
            return round(rating, 3)
        return
    get_rating.admin_order_field = 'rating'
    get_rating.short_description = _('Rating')

    def get_most_common_words_from_replies(self):
        """Determining most common words presents in replies."""

        # get all words in advantages and disadvantages of reply as two-nested list
        all_words = self.replies.values_list('advantages', 'disadvantages')

        # flat the two-nested list to single list
        all_words = flatten(all_words)

        # get 10 most common words with counters
        most_common_words = collections.Counter(all_words).most_common(10)

        # leave only words, without counters
        return ', '.join(i for i, j in most_common_words)
    get_most_common_words_from_replies.short_description = _('Most common words from replies')
