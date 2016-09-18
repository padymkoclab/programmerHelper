
from django.db import models


class MarkQuerySet(models.QuerySet):

    def objects_with_count_marks(self):
        """ """

        return self.annotate(count_marks=models.Count('marks', distinct=True))
