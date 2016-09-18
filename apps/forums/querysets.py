
from django.db import models


class ForumQuerySet(models.QuerySet):

    def forum_with_all_annotated_fields(self):
        """ """

        return self


class TopicQuesrySet(models.QuerySet):
    """Custom quesryset for managment filter/exclude topics of forum."""

    def topics_with_count_posts(self):
        """Topics with new field 'count_posts', where storing count posts certain topic."""

        return self.annotate(count_posts=models.Count('posts', distinct=True))

    def popular_topics(self):
        """Filter popular topics.
        Popular topic is a topic with 500 and more views and count posts must be 8 and more."""

        topics_with_count_posts = self.topics_with_count_posts()
        return topics_with_count_posts.filter(views__gte=500).filter(count_posts__gte=8)
