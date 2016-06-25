
import urllib

from django.db import models


class ArticleManager(models.Manager):
    """
    Model manager for articles.
    """

    def publish_articles_if_yet_not(self, article):
        """Publish article if it yet not."""

        self.filter(pk=article.pk).update(status=self.model.STATUS_ARTICLE.published)

    def made_articles_as_draft_if_yet_not(self, article):
        """Mark article as draft if yet not."""

        self.filter(pk=article.pk).update(status=self.model.STATUS_ARTICLE.draft)

    def check_exists_external_resourses_in_non_own_articles(self):
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


class PublishedArticleManager(models.Manager):
    """
    Model manager for only published articles.
    """


class DraftArticleManager(models.Manager):
    """
    Model manager for only published articles.
    """
# file:///media/wlysenko/66ABF2AC3D03BAAA/Web/Docs/Django_docs1.9/topics/db/managers.html?highlight=manager#calling-custom-queryset-methods-from-the-manager
