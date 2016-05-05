
from django.db import models


class TagManager(models.Manager):
    """
    Custom manager of tags for using tags in project.
    """

    def add(self, *args):
        pass
