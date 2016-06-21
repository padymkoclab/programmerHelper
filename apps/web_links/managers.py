
from django.db import models


class WebLinkManager(models.Manager):
    """
    Manager for web links.
    """

    def get_total_count_usage_weblinks_in_solutions(self):
        """Return total count usage web links in solutions."""

        self = self.annotate(count_solutions=models.Count('solutions'))
        self = self.aggregate(count_usage_solutions=models.Sum('count_solutions'))
        return self['count_usage_solutions']

    def get_total_count_usage_weblinks_in_articles(self):
        """Return total count usage web links in articles."""

        self = self.annotate(count_articles=models.Count('articles'))
        self = self.aggregate(count_usage_articles=models.Sum('count_articles'))
        return self['count_usage_articles']

    def get_statistics_usage_web_links(self):
        """Return statistics by usage a web links other objects.
        Statistics is returned as distionary, where a key is type of object
        and value is count usage the web links its type objects."""

        return {
            'count_usage_in_solutions': self.get_total_count_usage_weblinks_in_solutions(),
            'count_usage_in_articles': self.get_total_count_usage_weblinks_in_articles(),
        }
