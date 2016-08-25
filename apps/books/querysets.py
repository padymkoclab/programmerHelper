
from django.utils import timezone
from django.db import models

from psycopg2.extras import NumericRange

from mylabour.functions_db import Round
from mylabour.utils import create_logger_by_filename


logger = create_logger_by_filename(__name__)
NOW_YEAR = timezone.datetime.now().year


class BookQuerySet(models.QuerySet):
    """
    Queryset for books.
    """

    def books_with_count_tags(self):
        """Queryset with count tags of each the book."""

        return self.annotate(count_tags=models.Count('tags', distinct=True))

    def books_with_count_replies(self):
        """Queryset with count replies of each the book."""

        return self.annotate(count_replies=models.Count('replies', distinct=True))

    def books_with_rating(self):
        """Queryset with rating of each the book."""

        logger.debug('Is is working is not properly')

        # getting replies total sum all of the scopes
        self = self.values('replies').annotate(
            sum_scope=models.F('replies__scope_for_content') +
            models.F('replies__scope_for_style') +
            models.F('replies__scope_for_language')
        )

        # determining avg scope
        self = self.annotate(total_scope=models.ExpressionWrapper(
            models.F('sum_scope') / models.Value(3.0), output_field=models.FloatField()
        ))

        # make round for avg scope
        self = self.annotate(rating=Round('total_scope'))

        return self

    def books_with_count_tags_replies_and_rating(self):
        """Complex queryset with count tags, replies and rating of each the book."""

        return self.books_with_count_tags().books_with_count_replies().books_with_rating()

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


class WriterQuerySet(models.QuerySet):
    """
    Queryset for writers
    """

    def writers_with_count_books(self):
        """Determinating count books on each writer."""

        return self.annotate(count_books=models.Count('books', distinct=True))

    def writers_last_century(self):
        """Writers livig in the last century.
        If writer born early than 110 year ago, he must be have without fail year of death."""

        # find writer without year of death and
        # either without year of birth or if year of birth is early than 100 year ago.
        pks = list()
        for i in self.iterator():
            if i.years_life.upper is None:
                if i.years_life.lower is None or i.years_life.lower < NOW_YEAR - 100:
                    pks.append(i.pk)

        # exclude unsatisfied writers
        self = self.exclude(pk__in=pks)

        # filter only writers with living from 100 years ago to now
        self = self.filter(years_life__overlap=NumericRange(NOW_YEAR - 101, NOW_YEAR))
        return self

    def writers_with_avg_scope_by_rating_of_books(self):
        """ """

        raise NotImplementedError

    def writers_with_count_books_and_avg_scope_by_rating_of_books(self):
        """ """

        raise NotImplementedError
