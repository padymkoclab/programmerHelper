
from django.db import models


class ArticleQuerySet(models.QuerySet):
    """

    """

    def new_articles(self):
        """Articles published for last week."""

        pass

    def big_articles(self):
        """Article with count words 10000 and more."""

        pass

    def small_articles(self):
        """Article with count words until or equal 1000."""

        pass
