
import logging

from django.db import models

from utils.django.sql import NullsLastQuerySet


logger = logging.getLogger('django.development')


class SectionQuerySet(models.QuerySet):

    def sections_with_count_forums(self):
        """ """

        return self.annotate(count_forums=models.Count('forums', distinct=True))

    def sections_with_total_count_topics(self):
        """ """

        return self.annotate(total_count_topics=models.Count('forums__topics', distinct=True))

    def sections_with_total_count_posts(self):
        """ """

        return self.annotate(total_count_posts=models.Count('forums__topics__posts', distinct=True))

    def sections_with_all_annotated_fields(self):
        """ """

        self = self.sections_with_count_forums()
        self = self.sections_with_total_count_topics()
        self = self.sections_with_total_count_posts()

        return self


class ForumQuerySet(models.QuerySet):

    def forums_with_count_topics(self):
        """ """

        return self.annotate(count_topics=models.Count('topics', distinct=True))

    def forums_with_total_count_posts(self):
        """ """

        return self.annotate(total_count_posts=models.Count('topics__posts', distinct=True))

    def forums_with_count_active_users(self):
        """ """

        logger.error('"forums_with_count_active_users" working is not correct.')

        return self.annotate(
            count_topics_user=models.Count('topics__user', distinct=True),
            count_topics_posts_user=models.Count('topics__posts__user', distinct=True),
        ).annotate(
            count_active_users=models.F('count_topics_user') + models.F('count_topics_posts_user')
        )

    def forums_with_all_annotated_fields(self):
        """ """

        self = self.forums_with_count_topics()
        self = self.forums_with_total_count_posts()
        self = self.forums_with_count_active_users()

        return self


class TopicQuesrySet(models.QuerySet):
    """Custom quesryset for managment filter/exclude topics of forum."""

    def topics_with_count_posts(self):
        """Topics with new field 'count_posts', where storing count posts certain topic."""

        return self.annotate(count_posts=models.Count('posts', distinct=True))

    def topics_with_count_active_users(self):
        """Topics with new field 'count_posts', where storing count posts certain topic."""

        return self.annotate(count_active_users=models.Count('posts__user', distinct=True))

    def popular_topics(self):
        """Filter popular topics.
        Popular topic is a topic with 500 and more views and count posts must be 8 and more."""

        topics_with_count_posts = self.topics_with_count_posts()
        return topics_with_count_posts.filter(views__gte=500).filter(count_posts__gte=8)

    def topics_with_all_annotated_fields(self):
        """ """

        self = self.topics_with_count_posts()
        self = self.topics_with_count_active_users()

        return self


class UserForumQuerySet(NullsLastQuerySet):
    """

    """

    def users_with_count_topics(self):
        """ """

        return self.annotate(count_topics=models.Count('topics', distinct=True))

    def users_with_count_posts(self):
        """ """

        return self.annotate(count_posts=models.Count('posts', distinct=True))

    def users_with_count_popular_topic(self):
        """ """

        from .models import Topic

        return self.extra(
            select={
                'count_popular_topics': """
                SELECT
                    SUM(
                        CASE
                            WHEN {topic_table_name}."count_views" >= 500 THEN 1
                            ELSE 0
                        END
                    )
                FROM {topic_table_name}
                WHERE {user_table_name}."id" = {topic_table_name}."user_id"
                """.format(
                    user_table_name=self.model._meta.db_table,
                    topic_table_name=Topic._meta.db_table,
                )
            }
        )

    def users_with_date_latest_activity(self):

        return self.annotate(
            date_latest_updated_post=models.Max('posts__updated'),
            date_latest_updated_topic=models.Max('topics__updated')
        ).annotate(
            date_latest_activity_on_forums=models.functions.Greatest(
                'date_latest_updated_post', 'date_latest_updated_topic'
            )
        )

    def users_with_count_posts_topic_popular_topic_and_date_latest_activity_on_forums(self):

        self = self.users_with_count_topics()
        self = self.users_with_count_posts()
        self = self.users_with_count_popular_topic()
        self = self.users_with_date_latest_activity()

        return self
