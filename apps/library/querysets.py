
import logging

from django.db import models

logger = logging.getLogger('django.development')


class BookQuerySet(models.QuerySet):
    """
    Queryset for books.
    """

    def books_with_count_tags(self):
        """ """

        return self.prefetch_related('tags').annotate(
            count_tags=models.Count('tags', distinct=True)
        )

    def books_with_additional_fields(self):
        """Complex queryset with count tags, replies and rating of each the book."""

        self = self.books_with_count_tags()

        self = self.prefetch_related('replies').annotate(
            count_replies=models.Count('replies', distinct=True)
        )

        self = self.books_with_rating()

        return self

    def books_with_rating(self):
        """ """

        replies_table = self.model._meta.get_field('replies').rel.model._meta.db_table
        current_table = self.model._meta.db_table
        return self.extra(select={
            'rating': """
            SELECT
                ROUND(
                    AVG(
                        (
                            ("{replies_table}"."mark_for_content" +
                            "{replies_table}"."mark_for_style") +
                            "{replies_table}"."mark_for_language"
                        ) / 3.0
                    ), 3
                )
            FROM
                "{replies_table}"
            WHERE
                "{replies_table}"."object_id" = "{current_table}"."id"
            """.format(
                replies_table=replies_table,
                current_table=current_table,
            )
        })

    def get_great_books(self):
        """Books with count pages 500 and more."""

        return self.filter(count_pages__gte=1000)

    def get_big_books(self):
        """Books with count pages from 200 to 500."""

        return self.filter(count_pages__range=[300, 999])

    def get_middle_books(self):
        """Books with count pages from 50 to 200."""

        return self.filter(count_pages__range=[50, 299])

    def get_tiny_books(self):
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
        """ """

        return self.prefetch_related('books').annotate(count_books=models.Count('books', distinct=True))

    def writers_with_additional_fields(self):
        """Return queryset with annotated fields for each writer:
            - age
            - average mark by rating of books
            - count books
            - status of life"""

        self = self.writers_with_count_books()
        self = self.annotate(is_alive=models.Case(
            models.When(death_year=None, then=True),
            default=False,
            output_field=models.IntegerField()
        ))
        self = self.annotate(age=models.Case(
            models.When(death_year=None, then=models.Value(2016) - models.F('birth_year')),
            default=models.F('death_year') - models.F('birth_year'),
            output_field=models.IntegerField()
        ))

        logging.critical('A nested subquery does not working')

        # Writer.objects.extra(select={
        #     'avg_mark_for_books': """
        #     SELECT
        #         COUNT(DISTINCT "library_book"."id")
        #     FROM
        #         "library_book"
        #     GROUP BY
        #         "library_book"."id"
        #     """
        # }).values_list('avg_mark_for_books', flat=True)

        return self


class PublisherQuerySet(models.QuerySet):

    def publishers_with_count_books(self):
        """ """

        return self.prefetch_related('books').annotate(
            count_books=models.Count('books', distinct=True)
        )
