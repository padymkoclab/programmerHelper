
from django.db.models.functions import Greatest
from django.utils import timezone
from django.db import models


NOW_YEAR = timezone.datetime.now().year


class BookQuerySet(models.QuerySet):
    """
    Queryset for books
    """

    def books_with_count_tags(self):
        """Queryset with count tags of each the book."""

        return self.annotate(count_tags=models.Count('tags', distinct=True))

    def books_with_count_links(self):
        """Queryset with count links where are ability downloads of each with the book."""

        return self.annotate(count_links=models.Count('links', distinct=True))

    def books_with_count_replies(self):
        """Queryset with count replies of each the book."""

        return self.annotate(count_replies=models.Count('replies', distinct=True))

    def books_with_rating(self):
        """Queryset with rating of each the book."""

        return self.annotate(rating_avg=models.Avg('scopes__scope')).annotate(rating=Greatest('rating_avg', models.Value(0)))

    def books_with_count_tags_links_replies_and_rating(self):
        """Complex queryset with count tags, links, replies and rating of each the book."""

        return self.books_with_count_tags().books_with_count_links().\
            books_with_count_replies().books_with_rating()

    def new_books(self):
        """Books published no later in this and past year."""

        return self.filter(year_published__gte=NOW_YEAR - 1).filter(year_published__lte=NOW_YEAR)

    def giant_books(self):
        """Books with pages 500 and more."""

        return self.filter(pages__gte=500)

    def big_books(self):
        """Books with pages from 200 to 500."""

        return self.filter(pages__range=[200, 499])

    def middle_books(self):
        """Books with pages from 50 to 200."""

        return self.filter(pages__range=[50, 199])

    def tiny_books(self):
        """Books with pages until 50."""

        return self.filter(pages__lt=50)

    def books_with_sizes(self):
        """Queryset where each the book have determined values it size."""

        return self.annotate(size=models.Case(
            models.When(pk__in=self.giant_books(), then=models.Value('Giant book')),
            models.When(pk__in=self.big_books(), then=models.Value('Big book')),
            models.When(pk__in=self.middle_books(), then=models.Value('Middle book')),
            models.When(pk__in=self.tiny_books(), then=models.Value('Tiny book')),
            output_field=models.CharField(),
        ))


class WritterQuerySet(models.QuerySet):
    """

    """

    def writters_with_count_books(self):
        """Determinating count books on each writter."""

        return self.annotate(
            count_books=models.Count('books', distinct=True),
        )

    def living_writters(self):
        return self.filter(deathyear__isnull=True)

    def writters_lived_in_range_years(self, start_year, end_year=NOW_YEAR):
        """Find writter lived in certain range years."""

        z = []
        accepted_range = frozenset(range(start_year, end_year + 1))
        for i in self.iterator():
            q = i.deathyear
            if q is None:
                q = NOW_YEAR
            a = frozenset(range(i.birthyear, q + 1))
            if a & accepted_range:
                z.append(i.pk)
        return self.filter(pk__in=z)
