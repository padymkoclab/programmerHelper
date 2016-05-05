
from django.db import models


class Manager(models.Manager):
    """
    Model manager for working with atricles
    """

    def get_scope(self):
        pass
