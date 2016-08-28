
import re

from django.utils import timezone
from django.db import models

from mylabour.functions_db import Round
from mylabour.logging_utils import create_logger_by_filename


logger = create_logger_by_filename(__name__)


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

        self = self.annotate(total_mark_reply=(
            models.F('replies__mark_for_content') +
            models.F('replies__mark_for_language') +
            models.F('replies__mark_for_style')
        ) / models.Value(3))

        self = self.annotate(rating=models.functions.Coalesce(models.F('total_mark_reply'), 0.0))
        self = self.annotate(rating=Round('rating'))
        self = self.annotate(rating=models.Avg('rating'))
        self = self.annotate(rating=Round('rating'))

        logger.error('It is worked not properly yet')

        return self

    def books_with_count_tags_replies_and_rating(self):
        """Complex queryset with count tags, replies and rating of each the book."""

        logger.error('It is worked not properly yet')

        return self.books_with_count_tags().books_with_count_replies().books_with_rating()

    def new_books(self):
        """Books published in this or past year."""

        now_year = timezone.now().year
        return self.filter(year_published__gte=now_year - 1).filter(year_published__lte=now_year)

    def great_books(self):
        """Books with count pages 500 and more."""

        return self.filter(count_pages__gte=1000)

    def big_books(self):
        """Books with count pages from 200 to 500."""

        return self.filter(count_pages__range=[300, 999])

    def middle_books(self):
        """Books with count pages from 50 to 200."""

        return self.filter(count_pages__range=[50, 299])

    def tiny_books(self):
        """Books with count pages until 50."""

        return self.filter(count_pages__lt=50)

    def books_with_sizes(self):
        """Queryset where each the book have determined values it size."""

        return self.annotate(size=models.Case(
            models.When(pk__in=self.great_books(), then=models.Value('great')),
            models.When(pk__in=self.big_books(), then=models.Value('big')),
            models.When(pk__in=self.middle_books(), then=models.Value('middle')),
            models.When(pk__in=self.tiny_books(), then=models.Value('tiny')),
            output_field=models.CharField(),
        ))

    def popular_books(self):
        """Books with rating 5 and more."""

        logger.info('Add evaluation replated with Count Views of Book page')

        self = self.books_with_rating()
        return self.filter(rating__range=[4, 5])

    def books_wrote_on_english(self):
        """Book wrote on english."""

        return self.filter(language__exact='en')

    def books_wrote_on_russian(self):
        """Book wrote on russian."""

        return self.filter(language__exact='ru')


class WriterQuerySet(models.QuerySet):
    """
    A queryset for the model Writer
    """

    def writers_with_count_books(self):
        """Determinating count books on each writer."""

        return self.annotate(count_books=models.Count('books', distinct=True))

    def writers_with_age(self):
        """Annotate writers and deternimate age of each writer if it is possible."""

        return self.annotate(age=models.Case(
            models.When(death_year=None, then=models.Value(2016) - models.F('birth_year')),
            default=models.F('death_year') - models.F('birth_year'),
            output_field=models.IntegerField()
        ))

    def writers_with_status_life(self):
        """Annotate writers and deternimate age of each writer if it is possible."""

        return self.annotate(is_alive=models.Case(
            models.When(death_year=None, then=True),
            default=False,
            output_field=models.IntegerField()
        ))

    def writers_with_avg_mark_by_rating_of_books(self):
        """ """

        logger.error('NotImplementedError yet')
        return self

    def writers_with_count_books_and_avg_mark_by_rating_of_books(self):
        """ """

        logger.error('NotImplementedError yet')

        self = self.writers_with_count_books()
        self = self.writers_with_age()
        self = self.writers_with_status_life()
        self = self.writers_with_avg_mark_by_rating_of_books()
        return self
