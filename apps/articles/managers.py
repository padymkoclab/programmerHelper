
import urllib

from django.db import models

from utils.django.functions_db import Round

from apps.core.utils import get_statistics_count_objects_for_the_past_year, get_chart_count_objects_for_the_past_year


class ArticleManager(models.Manager):
    """
    Model manager for articles.
    """

    def check_exists_links(self):
        """Check exists external resourses in non own articles."""

        # get all non-own articles
        articles_from_external_resourse = self.articles_from_external_resourse()

        # return true if it not
        if not articles_from_external_resourse.count():
            return True

        # if found broken link
        # keep all the articles with broken links and return false,
        # otherwise return true
        article_with_broken_links = list()
        for article in articles_from_external_resourse:
            try:
                urllib.request.urlopen(article.source)
            except:
                article_with_broken_links.append(article)
        if article_with_broken_links:
            return (False, article_with_broken_links)
        return True

    def get_avg_count_subsections(self):
        """ """

        self = self.articles_with_count_subsections()
        return self.aggregate(avg=Round(models.Avg('count_subsections')))['avg']

    def get_statistics_count_articles_for_the_past_year(self):
        """ """

        return get_statistics_count_objects_for_the_past_year(self, 'date_added')

    def get_chart_count_articles_for_the_past_year(self):
        """ """

        return get_chart_count_objects_for_the_past_year(
            self.get_statistics_count_articles_for_the_past_year()
        )


class PublishedArticleManager(models.Manager):
    """
    Model manager for only published articles.
    """


class DraftArticleManager(models.Manager):
    """
    Model manager for only published articles.
    """
# file:///media/wlysenko/66ABF2AC3D03BAAA/Web/Docs/Django_docs1.9/topics/db/managers.html?highlight=manager#calling-custom-queryset-methods-from-the-manager
