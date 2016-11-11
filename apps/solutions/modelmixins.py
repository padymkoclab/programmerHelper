from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.django.functions_db import Round

from apps.tags.utils import get_favorite_tags


class SolutionModelMixin(object):
    """
    """

    def get_count_solutions(self):
        """ """

        if hasattr(self, 'count_solutions'):
            return self.count_solutions

        return self.solutions.count()
    get_count_solutions.admin_order_field = 'count_solutions'
    get_count_solutions.short_description = _('Count solutions')

    def get_favorite_tags_on_solutions(self):
        """ """

        qs_tags_pks = self.solutions.values_list('tags__pk', flat=True)
        favorite_tags = get_favorite_tags(qs_tags_pks)

        return favorite_tags
    get_favorite_tags_on_solutions.short_description = _('Favorite tag')

    def get_total_rating_on_solutions(self):
        """ """

        if hasattr(self, 'total_rating_solutions'):
            return self.total_rating_solutions

        solutions = self.solutions.annotate(rating=models.Sum(models.Case(
            models.When(opinions__is_useful=True, then=1),
            models.When(opinions__is_useful=False, then=-1),
            output_field=models.IntegerField()
        )))

        return solutions.aggregate(total_rating=Round(models.Avg('rating')))['total_rating']
    get_total_rating_on_solutions.admin_order_field = 'total_rating_solutions'
    get_total_rating_on_solutions.short_description = _('Total rating')

    def get_date_latest_solution(self):
        """ """

        if hasattr(self, 'date_latest_solution'):
            return self.date_latest_solution

        return self.solutions.aggregate(
            date_latest_solution=models.Max('created')
        )['date_latest_solution']
    get_date_latest_solution.admin_order_field = 'date_latest_solution'
    get_date_latest_solution.short_description = _('Latest solution')

    def get_count_comments_on_its_solutions(self):
        """ """

        if hasattr(self, 'count_comments_solutions'):
            return self.count_comments_solutions

        return self.solutions.aggregate(
            count_comments_solutions=models.Count('comments')
        )['count_comments_solutions'], self.count_comments_solutions
    get_count_comments_on_its_solutions.short_description = _('Count comments on solutions')
    get_count_comments_on_its_solutions.admin_order_field = 'count_comments_solutions'

    def get_count_opinions_on_solutions(self):

        if hasattr(self, 'count_opinions_solutions'):
            return self.count_opinions_solutions

        return self.solutions.aggregate(
            count_opinions_solutions=models.Count('opinions')
        )['count_opinions_solutions']
    get_count_opinions_on_solutions.short_description = _('Count opinions')
    get_count_opinions_on_solutions.admin_order_field = 'count_opinions_solutions'

    def get_count_good_opinions_on_solutions(self):

        if hasattr(self, 'count_good_opinions'):
            return self.count_good_opinions

        return self.solutions.filter(opinions__is_useful=True).count()
    get_count_good_opinions_on_solutions.admin_order_field = 'count_good_opinions'
    get_count_good_opinions_on_solutions.short_description = _('Count good opinions')

    def get_count_bad_opinions_on_solutions(self):

        if hasattr(self, 'count_bad_opinions'):
            return self.count_bad_opinions

        return self.solutions.filter(opinions__is_useful=False).count()
    get_count_bad_opinions_on_solutions.admin_order_field = 'count_bad_opinions'
    get_count_bad_opinions_on_solutions.short_description = _('Count bad opinions')
