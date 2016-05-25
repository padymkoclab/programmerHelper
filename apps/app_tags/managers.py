
from django.db import models

from mylabour.utils import get_random_objects


class TagQuerySet(models.QuerySet):
    """

    """

    def random_tags(self, count=1):
        return get_random_objects(self, count)


class TagManager(models.Manager):
    """
    Custom manager of tags for using tags in project.
    """

    pass
