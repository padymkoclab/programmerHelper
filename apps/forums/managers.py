
from django.db import models

from .querysets import TopicQuesrySet, ForumQuerySet


class ForumManager(models.Manager):
    """ """

    pass


class TopicManager(models.Manager):
    """
    Model manager for topics of forum
    """

    pass


ForumManager = ForumManager.from_queryset(ForumQuerySet)
TopicManager = TopicManager.from_queryset(TopicQuesrySet)
