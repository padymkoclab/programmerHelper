
from django.db import models

from mylabour.functions_db import Round


class ReplyQuerySet(models.QuerySet):
    """
    QuerySet for replies.
    """

    def replies_with_total_scope(self):
        """Determining average scope for each reply by their scopes: for content, for style, for language."""

        # getting total sum all of the scopes
        self = self.annotate(
            sum_scope=models.F('scope_for_content') + models.F('scope_for_style') + models.F('scope_for_language')
        )
        # determining avg scope
        self = self.annotate(total_scope=models.ExpressionWrapper(
            models.F('sum_scope') / models.Value(3.0), output_field=models.FloatField()
        ))
        # make round for avg scope
        self = self.annotate(total_scope=Round('total_scope'))
        return self
