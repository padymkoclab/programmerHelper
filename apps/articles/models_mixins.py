
from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.django.functions_db import Round

from apps.tags.utils import get_favorite_tags


class ArticleModelMixin(object):
    """

    """

    def get_count_comments_of_articles(self):
        """ """

        if hasattr(self, 'count_comments_articles'):
            return self.count_comments_articles

        return self.articles.aggregate(
            count_comments_articles=models.Count('comments', distinct=True)
        )['count_comments_articles']
    get_count_comments_of_articles.short_description = _('Count comments of articles')
    get_count_comments_of_articles.admin_order_field = 'count_comments_articles'

    def get_count_articles(self):
        """ """

        if hasattr(self, 'count_articles'):
            return self.count_articles

        return self.articles.count()
    get_count_articles.admin_order_field = 'count_articles'
    get_count_articles.short_description = _('Count article')

    def get_favorite_tags_of_articles(self):
        """ """

        qs_tags_pks = self.articles.values_list('tags__pk', flat=True)
        favorite_tags = get_favorite_tags(qs_tags_pks)

        return favorite_tags
    get_favorite_tags_of_articles.short_description = _('Favorite tag')

    def get_total_rating_of_articles(self):
        """ """

        if hasattr(self, 'total_rating_articles'):
            return self.total_rating_articles

        return self.articles.annotate(
            rating=models.Avg('marks__mark')
        ).aggregate(
            total_rating_articles=Round(models.Avg('rating'))
        )['total_rating_articles']
    get_total_rating_of_articles.admin_order_field = 'total_rating_articles'
    get_total_rating_of_articles.short_description = _('Total rating')

    def get_date_latest_article(self):
        """ """

        if hasattr(self, 'date_latest_article'):
            return self.date_latest_article

        try:
            return self.articles.latest().created
        except self.articles.model.DoesNotExist:
            return
    get_date_latest_article.admin_order_field = 'date_latest_article'
    get_date_latest_article.short_description = _('Latest article')

    def get_count_marks_of_articles(self):

        if hasattr(self, 'count_marks_articles'):
            return self.count_marks_articles

        return self.articles.aggregate(count_marks=models.Count('marks', distinct=True))['count_marks']
    get_count_marks_of_articles.short_description = _('Count marks')
    get_count_marks_of_articles.admin_order_field = 'count_marks_articles'
