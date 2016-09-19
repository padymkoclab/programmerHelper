
from django.db import models

from apps.core.utils import (
    get_statistics_count_objects_for_the_past_year,
    get_chart_count_objects_for_the_past_year,
)

from .querysets import SectionQuerySet, ForumQuerySet, TopicQuesrySet


class SectionManager(models.Manager):

    pass


class ForumManager(models.Manager):
    """ """

    pass


class TopicManager(models.Manager):
    """
    Model manager for topics of forum
    """


class PostManager(models.Manager):
    """
    Model manager for topics of forum
    """

    def get_statistics_count_posts_for_the_past_year(self):
        """ """

        return get_statistics_count_objects_for_the_past_year(self, 'date_added')

    def get_chart_count_posts_for_the_past_year(self):
        """ """

        return get_chart_count_objects_for_the_past_year(
            self.get_statistics_count_posts_for_the_past_year()
        )


SectionManager = SectionManager.from_queryset(SectionQuerySet)
ForumManager = ForumManager.from_queryset(ForumQuerySet)
TopicManager = TopicManager.from_queryset(TopicQuesrySet)
