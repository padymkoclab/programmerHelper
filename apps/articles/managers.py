
import collections
import urllib

from django.db import models

import pygal

from utils.django.functions_db import Round

from apps.core.utils import get_statistics_count_objects_for_the_past_year, get_chart_count_objects_for_the_past_year

from .querysets import ArticleQuerySet, SubsectionQuerySet


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


class MarkManager(models.Manager):
    """

    """

    def get_avg_count_marks_on_object(self):
        """ """

        self = self.objects_with_count_marks()
        return self.aggregate(avg=Round(
            models.functions.Coalesce(models.Avg('count_marks'), 0)
        ))['avg']

    def get_statistics_used_marks(self):
        """Return count a used tags on deternimed type objects."""

        marks = self.filter(marks__mark__isnull=False).values_list('marks__mark', flat=True)

        counter_marks = collections.Counter(marks)

        stat = [(mark, count) for mark, count in counter_marks.items()]

        stat.sort(key=lambda x: x[0])

        return stat

    def get_chart_used_marks(self):
        """ """

        stat = self.get_statistics_used_marks()

        config = pygal.Config(
            width=800,
            height=300,
            explicit_size=True,
            legend_box_size=5,
        )

        chart = pygal.HorizontalBar(config)

        for mark, count in stat:
            chart.add(str(mark), count)

        return chart.render()


ArticleManager = ArticleManager.from_queryset(ArticleQuerySet)
SubsectionManager = SubsectionQuerySet.as_manager
