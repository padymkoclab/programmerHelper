
from django.db import models


class OpinionQuerySet(models.QuerySet):

    def opinions_with_marks(self):
        """ """

        return self.annotate(mark=models.Case(
            models.When(is_useful=True, then=1),
            models.When(is_useful=False, then=-1),
            output_fields=models.IntegerField()
        )).annotate()
