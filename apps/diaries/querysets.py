
from django.utils import timezone
from django.db import models


class DiaryQuerySet(models.QuerySet):

    def diaries_with_count_partitions(self):
        """ """

        return self.annotate(count_partitions=models.Count('partitions', distinct=True))
