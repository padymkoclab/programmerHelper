
from django.db import models

from utils.django.functions_db import Round


class ReplyQuerySet(models.QuerySet):
    """
    QuerySet for replies.
    """

    def replies_with_total_mark(self):
        """Determining average mark for each reply by their marks: for content, for style, for language."""

        # getting total sum all of the marks
        self = self.annotate(
            total_mark=models.F('mark_for_content') + models.F('mark_for_style') + models.F('mark_for_language')
        )

        # determining avg mark
        self = self.annotate(total_mark=models.ExpressionWrapper(
            models.F('total_mark') / models.Value(3.0), output_field=models.FloatField()
        ))

        # make round for avg mark
        self = self.annotate(total_mark=Round('total_mark'))

        return self
