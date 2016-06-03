
from django.db import models


class ArticleManager(models.Manager):
    """
    Model manager for working with articles
    """

    def publish_articles_if_yet_not(self, article):
        """Publish article if it yet not."""

        return self.get_queryset().function()

    def send_articles_on_rework(self, article):
        """Mark article as draft and send it on rework."""

        return self.get_queryset().function()

    def check_exists_external_resourses_in_non_own_articles(self):
        """Check exists external resourses in non own articles."""

        pass
