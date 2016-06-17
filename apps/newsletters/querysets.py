
from django.db import models


class NewsQueryset(models.QuerySet):
    """

    """

    def news_for_week(self):
        """All news from website for week."""

        raise NotImplementedError

    def news_for_month(self):
        """All news from website for month."""

        raise NotImplementedError

    def news_about_snippets(self):
        """ """

        raise NotImplementedError
