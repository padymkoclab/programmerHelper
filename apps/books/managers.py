
from django.db import models


class BookManager(models.Manager):
    """
    Model manager
    """

    def popular_books_by_views(self):
        pass

# create managers
