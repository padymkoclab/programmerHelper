
from django.db import models


class CommentQuerySet(models.QuerySet):

    def objects_with_count_comments(self):
        """Added to each snippet new field with count of comments of the a each snippet."""

        return self.annotate(count_comments=models.Count('comments', distinct=True))
