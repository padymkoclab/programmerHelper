
from django.db import models


class SnippetQuerySet(models.QuerySet):
    """
    QuerySet for using with queryset model Snippet
    """

    def objects_with_marks(self):
        """Added to each snippet new field 'mark' where storage her mark."""

        return self.annotate(mark=models.Sum(
            models.Case(
                models.When(opinions__is_useful=True, then=1),
                models.When(opinions__is_useful=False, then=-1),
                default=0,
                output_field=models.IntegerField()
            )
        ))

    def snippets_with_count_tags(self):
        """Added to each snippet new field with count of tags of the a each snippet."""

        return self.annotate(count_tags=models.Count('tags', distinct=True))

    def snippets_with_count_opinions(self):
        """Added to each snippet new field with count of opinions of the a each snippet."""

        return self.annotate(count_opinions=models.Count('opinions', distinct=True))

    def snippets_with_count_comments(self):
        """Added to each snippet new field with count of comments of the a each snippet."""

        return self.annotate(count_comments=models.Count('comments', distinct=True))

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

    def snippets_with_total_counters_on_related_fields(self):
        """Determinating for each snippet count_tags, opinions, favours, comments,
        getting mark, count good/bad opinions, and count likes/dislikes favours."""

        self = self.objects_with_marks()
        self = self.snippets_with_count_tags()
        self = self.snippets_with_count_comments()
        self = self.snippets_with_count_opinions()
        self = self.snippets_with_count_favours()
        self = self.snippets_with_count_like_favours()
        self = self.snippets_with_count_dislike_favours()
        return self
