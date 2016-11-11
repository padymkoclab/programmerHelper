
from django.utils.translation import ugettext_lazy as _
from django.db import models

from utils.django.functions_db import Round

from apps.tags.utils import get_favorite_tags


class SnippetModelMixin(object):
    """
    """

    def get_count_snippets(self):
        """ """

        if hasattr(self, 'count_snippets'):
            return self.count_snippets

        return self.snippets.count()
    get_count_snippets.admin_order_field = 'count_snippets'
    get_count_snippets.short_description = _('Count snippets')

    def get_favorite_tags_on_snippets(self):
        """ """

        qs_tags_pks = self.snippets.values_list('tags__pk', flat=True)
        favorite_tags = get_favorite_tags(qs_tags_pks)

        return favorite_tags
    get_favorite_tags_on_snippets.short_description = _('Favorite tag')

    def get_total_rating_on_snippets(self):
        """ """

        if hasattr(self, 'total_rating_snippets'):
            return self.total_rating_snippets

        snippets = self.snippets.annotate(rating=models.Sum(models.Case(
            models.When(opinions__is_useful=True, then=1),
            models.When(opinions__is_useful=False, then=-1),
            output_field=models.IntegerField()
        )))

        return snippets.aggregate(
            total_rating_snippets=Round(models.Avg('rating'))
        )['total_rating_snippets']
    get_total_rating_on_snippets.admin_order_field = 'total_rating_snippets'
    get_total_rating_on_snippets.short_description = _('Total rating')

    def get_date_latest_snippet(self):
        """ """

        if hasattr(self, 'date_latest_snippet'):
            return self.date_latest_snippet

        return self.snippets.aggregate(
            date_latest_snippet=models.Max('created')
        )['date_latest_snippet']
    get_date_latest_snippet.admin_order_field = 'date_latest_snippet'
    get_date_latest_snippet.short_description = _('Latest snippet')

    def get_count_comments_on_its_snippets(self):
        """ """

        if hasattr(self, 'count_comments_snippets'):
            return self.count_comments_snippets

        return self.snippets.aggregate(
            count_comments_snippets=models.Count('comments')
        )['count_comments_snippets'], self.count_comments_snippets
    get_count_comments_on_its_snippets.short_description = _('Count comments on snippets')
    get_count_comments_on_its_snippets.admin_order_field = 'count_comments_snippets'

    def get_count_opinions_on_snippets(self):

        if hasattr(self, 'count_opinions_snippets'):
            return self.count_opinions_snippets

        return self.snippets.aggregate(
            count_opinions_snippets=models.Count('opinions')
        )['count_opinions_snippets']
    get_count_opinions_on_snippets.short_description = _('Count opinions')
    get_count_opinions_on_snippets.admin_order_field = 'count_opinions_snippets'

    def get_count_good_opinions_on_snippets(self):

        if hasattr(self, 'count_good_opinions_snippets'):
            return self.count_good_opinions_snippets

        return self.snippets.filter(opinions__is_useful=True).count()
    get_count_good_opinions_on_snippets.short_description = _('count good opinions')
    get_count_good_opinions_on_snippets.admin_order_field = 'count_good_opinions_snippets'

    def get_count_bad_opinions_on_snippets(self):

        if hasattr(self, 'count_bad_opinions_snippets'):
            return self.count_bad_opinions_snippets

        return self.snippets.filter(opinions__is_useful=False).count()
    get_count_bad_opinions_on_snippets.short_description = _('count bad opinions')
    get_count_bad_opinions_on_snippets.admin_order_field = 'count_bad_opinions_snippets'
