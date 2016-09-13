
from django.db import models


class FlavourManager(models.Manager):
    """
    Manager for other models
    """

    def get_count_flavours(self):
        """ """

        return self.filter(flavours__isnull=False).values('flavours').count()
