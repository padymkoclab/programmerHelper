
from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.django.functions_db import Round

from apps.tags.utils import get_favorite_tags


class ArticleModelMixin(object):
    """
    """

    def get_count_articles(self):
        """ """

        if hasattr(self, 'count_articles'):
            return self.count_articles

        return self.articles.count()
    get_count_articles.admin_order_field = 'count_articles'
    get_count_articles.short_description = _('Count article')

    def get_favorite_tags_on_articles(self):
        """ """

        qs_tags_pks = self.articles.values_list('tags__pk', flat=True)
        favorite_tags = get_favorite_tags(qs_tags_pks)

        return favorite_tags
    get_favorite_tags_on_articles.short_description = _('Favorite tag')

    def get_total_rating_on_articles(self):
        """ """

        if hasattr(self, 'total_rating_articles'):
            return self.total_rating_articles

        return self.articles.annotate(
            rating=models.Avg('marks__mark')
        ).aggregate(
            total_rating_articles=Round(models.Avg('rating'))
        )['total_rating_articles']
    get_total_rating_on_articles.admin_order_field = 'total_rating_articles'
    get_total_rating_on_articles.short_description = _('Total rating')

    def get_date_latest_article(self):
        """ """

        if hasattr(self, 'date_latest_article'):
            return self.date_latest_article

        return self.articles.aggregate(
            date_latest_article=models.Max('created')
        )['date_latest_article']
    get_date_latest_article.admin_order_field = 'date_latest_article'
    get_date_latest_article.short_description = _('Latest article')

    def get_count_marks_on_articles(self):

        if hasattr(self, 'count_marks_articles'):
            return self.count_marks_articles

        return self.articles.aggregate(count_marks=models.Count('marks', distinct=True))['count_marks']
    get_count_marks_on_articles.short_description = _('Count marks')
    get_count_marks_on_articles.admin_order_field = 'count_marks_articles'

    def get_count_comments_on_its_articles(self):
        """ """

        if hasattr(self, 'count_comments_articles'):
            return self.count_comments_articles

        return self.articles.aggregate(
            count_comments_articles=models.Count('comments', distinct=True)
        )['count_comments_articles'], self.count_comments_articles
    get_count_comments_on_its_articles.short_description = _('Count comments on articles')
    get_count_comments_on_its_articles.admin_order_field = 'count_comments_articles'


class UserMarkModelMixin(object):
    """
    """

    def get_total_count_marks(self):

        if hasattr(self, 'total_count_marks'):
            return self.total_count_marks

        return self.marks.count()
    get_total_count_marks.short_description = _('Total count marks')
    get_total_count_marks.admin_order_field = 'total_count_marks'

    def get_date_latest_mark(self):

        if hasattr(self, 'date_latest_mark'):
            return self.date_latest_mark

        return self.marks.aggregate(
            date_latest_mark=models.Max('created')
        )['date_latest_mark']
    get_date_latest_mark.short_description = _('Date latest mark')
    get_date_latest_mark.admin_order_field = 'date_latest_mark'

    def get_article_with_latest_mark_and_admin_url(self):

        from .models import Article

        if hasattr(self, 'latest_mark_article_id'):
            if self.latest_mark_article_id is None:
                return
            return Article._default_manager.get(pk=self.latest_mark_article_id)

        latest_mark = self.marks.order_by('-created').first()
        return None if latest_mark is None else latest_mark.article
    get_article_with_latest_mark_and_admin_url.short_description = _('Article with latest mark')
    get_article_with_latest_mark_and_admin_url.with_change_admin_url = True
