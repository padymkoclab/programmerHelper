
from django.db import models


class ArticleQuerySet(models.QuerySet):
    """

    """

    pass

    # def find_articles_without_tags_and_links(self):
    #     """ """

    #     return self.get_queryset().function()


class ArticleManager(models.Manager):
    """
    Model manager for working with articles
    """

    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def articles_with_rating(self):
        return self.annotate(rating=models.Avg('scopes__scope'))



