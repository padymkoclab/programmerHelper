
from django.utils import timezone
from django.db import models

from psycopg2.extras import NumericRange

from mylabour.functions_db import Round


NOW_YEAR = timezone.datetime.now().year


class BookQuerySet(models.QuerySet):
    """
    Queryset for books.
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

        raise NotImplementedError

        self = self.annotate(rating=models.Avg('replies__scope_for_content'))
        self = self.annotate(rating=models.functions.Coalesce('rating', .0))
        self = self.annotate(rating=Round('rating'))
        return self

    def books_with_count_tags_links_replies_and_rating(self):
        """Complex queryset with count tags, links, replies and rating of each the book."""

        return self.books_with_count_tags().books_with_count_links().books_with_count_replies().books_with_rating()

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

    def popular_books(self):
        """Books with rating 5 and more."""

        #
        # Rating and count views page
        #

        self = self.books_with_rating()
        return self.filter(rating__range=[4, 5])

    def books_wrote_english(self):
        """Book wrote on english."""

        return self.filter(language__iexact='en')

    def books_wrote_non_english(self):
        """Book wrote non english."""

        return self.exclude(language__iexact='en')


class WritterQuerySet(models.QuerySet):
    """
    Queryset for writters
    """

    def writters_with_count_books(self):
        """Determinating count books on each writter."""

        return self.annotate(count_books=models.Count('books', distinct=True))

    def writters_last_century(self):
        """Writters livig in the last century.
        If writter born early than 110 year ago, he must be have without fail year of death."""

        # find writter without year of death and
        # either without year of birth or if year of birth is early than 100 year ago.
        pks = list()
        for i in self.iterator():
            if i.years_life.upper is None:
                if i.years_life.lower is None or i.years_life.lower < NOW_YEAR - 100:
                    pks.append(i.pk)

        # exclude unsatisfied writters
        self = self.exclude(pk__in=pks)

        # filter only writters with living from 100 years ago to now
        self = self.filter(years_life__overlap=NumericRange(NOW_YEAR - 101, NOW_YEAR))
        return self

    def writters_with_avg_scope_by_rating_of_books(self):
        """ """

        raise NotImplementedError

    def writters_with_count_books_and_avg_scope_by_rating_of_books(self):
        """ """

        raise NotImplementedError
