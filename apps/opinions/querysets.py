
from django.db import models


class OpinionQuerySet(models.QuerySet):

    def objects_with_count_opinions(self):
        """ """

        return self.annotate(count_opinions=models.Count('opinions', distinct=True))
