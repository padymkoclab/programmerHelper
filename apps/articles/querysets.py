
from django.db import models


class ArticleQuerySet(models.QuerySet):
    """

    """

    def articles_with_rating(self):
        """Adding for each the article field with determined rating of an itself."""

        pass

    def articles_with_count_comments(self):
        """Adding for each the article field with determined rating of an itself."""

        pass

    def articles_with_count_tags(self):
        """Adding for each the article field with determined rating of an itself."""

        pass

    def articles_with_count_links(self):
        """Adding for each the article field with determined rating of an itself."""

        pass

    def articles_with_count_subsections(self):
        """Adding for each the article field with determined rating of an itself."""

        pass

    def articles_with_rating_and_count_comments_subsections_tags_links(self):
        """Adding for each the article field with determined rating of an itself."""

        pass

    def published_articles(self):
        """Articles already published."""

        pass

    def draft_articles(self):
        """Articles yet not published."""

        pass

    def weekly_articles(self):
        """Articles published for last week."""

        pass

    def big_articles(self):
        """Articles with count words 10000 and more."""

        pass

    def small_articles(self):
        """Articles with count words until or equal 1000."""

        pass

    def articles_from_external_resourse(self):
        """Articles from external resourse pinted in field 'source'."""

        pass

    def own_articles(self):
        """Own articles, published from website`s authors."""

        pass

    def hot_articles(self):
        """Articles with many comments."""

        pass

    def popular_articles(self):
        """Articles with high rating."""

        pass

    def latest_articles(self):
        """Articles latest added."""

        pass
