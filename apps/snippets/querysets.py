
from django.db import models

from apps.opinions.utils import annotate_queryset_for_determinate_rating


class SnippetQuerySet(models.QuerySet):
    """
    QuerySet for using with queryset model Snippet
    """

    def snippets_by_marks(self, min_mark=None, max_mark=None):
        """Snippets with certain range of marks."""

        objects_with_marks = self.objects_with_marks()
        if min_mark is not None and max_mark is None:
            return objects_with_marks.filter(mark__gte=min_mark)
        elif min_mark is None and max_mark is not None:
            return objects_with_marks.filter(mark__lte=max_mark)
        elif min_mark is not None and max_mark is not None:
            return objects_with_marks.filter(mark__gte=min_mark).filter(mark__lte=max_mark)
        else:
            raise TypeError('Missing 1 required argument: "min_mark" or "max_mark".')

    def snippets_with_count_favours(self):
        """Added to each snippet new field with count of favours of the each snippet."""

        return self.annotate(count_favours=models.Count('favours', distinct=True))

    def snippets_with_count_like_favours(self):
        """Added to each snippet new field with count of liked favours of the each snippet."""

        return self.annotate(count_like_favours=models.Sum(
            models.Case(
                models.When(favours__is_favour=True, then=1),
                default=0,
                output_field=models.IntegerField()
            )
        ))

    def snippets_with_count_dislike_favours(self):
        """Added to each snippet new field with count of disliked favours of the each snippet."""

        return self.annotate(count_dislike_favours=models.Sum(
            models.Case(
                models.When(favours__is_favour=False, then=1),
                default=0,
                output_field=models.IntegerField()
            )
        ))

    def snippets_with_all_additional_fields(self):
        """Determinating for each snippet count_tags, opinions, favours, comments,
        getting mark, count good/bad opinions, and count likes/dislikes favours."""

        self = self.annotate(count_tags=models.Count('tags', distinct=True))

        self = self.annotate(count_opinions=models.Count('opinions', distinct=True))

        self = self.annotate(count_comments=models.Count('comments', distinct=True))

        self = annotate_queryset_for_determinate_rating(self)

        return self
