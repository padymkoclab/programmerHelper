
from django.db import models

from utils.django.functions_db import Round


class CategoryManager(models.Manager):

    def get_avg_count_utilities(self):
        """ """

        self = self.categories_with_count_utilities()
        avg = self.aggregate(avg=Round(models.Avg('count_utilities')))['avg']
        return avg or 0


class UtilityManager(models.Manager):

    def get_count_opinions(self):
        """ """

        self = self.utilities_with_count_opinions()
        count_opinions = self.aggregate(sum=models.Sum('count_opinions'))['sum']
        return count_opinions or 0
