
from django.utils import timezone
from django.db import models


class DiaryQuerySet(models.QuerySet):

    def diaries_with_count_partitions(self):
        """ """

        return self.annotate(count_partitions=models.Count('partitions', distinct=True))

    def diaries_with_date_latest_changes(self):
        """ """

        return self.annotate(date_latest_changes=models.Max('partitions__updated'))

    def diaries_with_total_size(self):
        """ """

        return self.annotate(total_size=models.Sum(models.functions.Length('partitions__content')))

    def diaries_with_all_annotated_fields(self):
        """ """

        self = self.diaries_with_count_partitions()
        self = self.diaries_with_total_size()
        self = self.diaries_with_date_latest_changes()

        return self
