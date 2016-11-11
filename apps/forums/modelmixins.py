
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserForumModelMixin(object):
    """
    """

    def get_count_posts(self):
        """ """

        if hasattr(self, 'count_posts'):
            return self.count_posts

        return self.posts.count(), self.count_posts
    get_count_posts.admin_order_field = 'count_posts'
    get_count_posts.short_description = _('Count posts')

    def get_count_topics(self):
        """ """

        if hasattr(self, 'count_topics'):
            return self.count_topics

        return self.topics.count(), self.count_topics
    get_count_topics.admin_order_field = 'count_topics'
    get_count_topics.short_description = _('Count topics')

    def get_count_popular_topics(self):
        """Getting count popular topics of user."""

        if hasattr(self, 'count_popular_topics'):
            return self.count_popular_topics

        return self.topics.filter(count_views__gte=500).count(), self.count_popular_topics
    get_count_popular_topics.admin_order_field = 'count_popular_topics'
    get_count_popular_topics.short_description = _('Сount popular topics')

    def get_date_latest_activity_on_forums(self):
        """ """

        if hasattr(self, 'date_latest_activity_on_forums'):
            return self.date_latest_activity_on_forums

        dates_latest_update_post_and_topic = (
            self.posts.aggregate(date=models.Max('updated'))['date'],
            self.topics.aggregate(date=models.Max('updated'))['date'],
        )

        if any(dates_latest_update_post_and_topic):
            return max(filter(lambda x: x is not None, dates_latest_update_post_and_topic))
        return
    get_date_latest_activity_on_forums.admin_order_field = 'date_latest_activity_on_forums'
    get_date_latest_activity_on_forums.short_description = _('Latest activity')
