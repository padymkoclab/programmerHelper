
import numbers

from django.utils import timezone
from django.db import models

from utils.django.functions_db import Round, ArrayLength
from utils.django.sql import NullsLastQuerySet


class ArticleQuerySet(models.QuerySet):
    """
    Suit methods for work with queryset of artices.
    """

    def objects_with_rating(self):
        """Adding for each the article field with determined rating of an itself."""

        self = self.defer('subsections').annotate(rating=models.Avg('marks__mark'))
        self = self.annotate(rating=Round('rating'))
        return self

    def articles_with_volume(self):
        """Adding for each the article field with determined volume of an itself.
        Volume of article determine on count characters in
        header, subsections and conclusion of the article."""

        self = self.annotate(count_characters_in_header=models.functions.Length('header'))
        self = self.annotate(count_characters_in_conclusion=models.functions.Length('conclusion'))
        self = self.annotate(count_characters_in_subsections=models.Sum(
            models.Case(
                models.When(subsections__content__isnull=False, then=models.functions.Length('subsections__content')),
                output_field=models.IntegerField(),
                default=0,
            )
        ))
        self = self.annotate(volume=models.F('count_characters_in_header') +
                             models.F('count_characters_in_conclusion') +
                             models.F('count_characters_in_subsections'))
        return self

    def articles_with_count_comments(self):
        """Adding for each the article field with determined count comments of an itself."""

        return self.defer('subsections').annotate(
            count_comments=models.Count('comments', distinct=True)
        )

    def articles_with_count_marks(self):
        """Adding for each the article field with determined count marks of an itself."""

        return self.defer('subsections').annotate(
            count_marks=models.Count('marks', distinct=True)
        )

    def articles_with_count_tags(self):
        """Adding for each the article field with determined count tags of an itself."""

        return self.defer('subsections').annotate(
            count_tags=models.Count('tags', distinct=True)
        )

    def articles_with_count_links(self):
        """Adding for each the article field with determined count useful links, used in each article."""

        return self.defer('subsections').annotate(
            count_links=ArrayLength('links', *(1, ))
        )

    def articles_with_count_subsections(self):
        """Adding for each the article field with determined count subsections of an itself."""

        return self.defer('subsections').annotate(
            count_subsections=models.Count('subsections', distinct=True)
        )

    def articles_with_all_additional_fields(self):
        """Determining for each article: count tags, comments, links, marks, subsections and rating."""

        self = self.objects_with_rating()
        self = self.articles_with_count_comments()
        self = self.articles_with_count_marks()
        self = self.articles_with_count_tags()
        self = self.articles_with_count_links()
        self = self.articles_with_count_subsections()
        return self

    def published_articles(self):
        """Articles already published."""

        return self.only('status').filter(status=self.model.STATUS_ARTICLE.published)

    def draft_articles(self):
        """Articles yet not published."""

        return self.only('status').filter(status=self.model.STATUS_ARTICLE.draft)

    def weekly_articles(self):
        """Articles published for last week."""

        return self.only('date_added').filter(
            date_added__range=[timezone.now() - timezone.timedelta(weeks=1), timezone.now()]
        )

    def articles_from_external_resourse(self):
        """Articles from external resourse pinted in field 'source'."""

        return self.only('source').filter(source__isnull=False)

    def own_articles(self):
        """Own articles, published from website`s authors."""

        return self.only('source').filter(source__isnull=True)

    def hot_articles(self):
        """Articles with 7 and more comments."""

        articles_with_count_comments = self.articles_with_count_comments()
        return articles_with_count_comments.filter(count_comments__gte=7)

    def popular_articles(self):
        """Articles with rating from 4 and more."""

        self = self.objects_with_rating()
        return self.filter(rating__gte=4)

    def articles_by_rating(self, min_rating=None, max_rating=None):
        """Filter articles by certain range of rating."""

        if min_rating is None and max_rating is None:
            raise TypeError('Please point at least either min_rating or max_rating.')
        self = self.objects_with_rating()
        if isinstance(min_rating, numbers.Real) and isinstance(max_rating, numbers.Real):
            if min_rating > max_rating:
                raise ValueError('Don`t right values: min_rating is more than max_rating.')
            return self.filter(rating__gte=min_rating).filter(rating__lte=max_rating)
        elif isinstance(min_rating, numbers.Real):
            return self.filter(rating__gte=min_rating)
        elif isinstance(max_rating, numbers.Real):
            return self.filter(rating__lte=max_rating)

    def big_articles(self):
        """Articles with count characters 10000 and more."""

        return self.articles_with_volume().filter(volume__gte=10000)


class SubsectionQuerySet(models.QuerySet):

    def subsections_with_length_of_content(self):
        """ """

        return self.annotate(content_length=models.functions.Length('content'))


class UserArticleQuerySet(NullsLastQuerySet):
    """

    """

    def users_with_count_articles(self):
        """ """

        return self.annotate(count_articles=models.Count('articles', distinct=True))

    def users_with_total_rating_on_articles(self):
        """Adding for each the article field with determined rating of an itself."""

        from .models import Mark, Article

        return self.defer('articles__subsections').extra(
            select={
                'total_rating_articles': """
                    SELECT
                        ROUND(AVG(R), 3)
                    FROM
                        (
                        SELECT
                            {article_table}."user_id",
                            (
                                SELECT AVG({mark_table}."mark") AS R
                                FROM {mark_table}
                                WHERE {mark_table}."article_id" = {article_table}."id"
                            )
                        FROM
                            {article_table}
                        ) AS ARTICLE_TABLE
                    WHERE ARTICLE_TABLE."user_id" = {user_table}."id"
                """.format(
                    mark_table=Mark._meta.db_table,
                    article_table=Article._meta.db_table,
                    user_table=self.model._meta.db_table,
                )
            },
        )

    def users_with_count_comments_on_articles(self):
        """Adding for each the article field with determined count comments of an itself."""

        return self.defer('articles__subsections').annotate(
            count_comments_articles=models.Count('articles__comments', distinct=True)
        )

    def users_with_count_marks_on_articles(self):
        """Adding for each the article field with determined count marks of an itself."""

        return self.defer('articles__subsections').annotate(
            count_marks_articles=models.Count('articles__marks', distinct=True)
        )

    def users_with_date_latest_article(self):
        """Adding for each the article field with determined count marks of an itself."""

        return self.defer('articles__subsections').annotate(
            date_latest_article=models.Max('articles__created')
        )

    def users_with_count_articles_comments_marks_and_rating_and_date_latest_articles(self):
        """Determining for each article: count tags, comments, links, marks, subsections and rating."""

        self = self.users_with_count_articles()
        self = self.users_with_total_rating_on_articles()
        self = self.users_with_count_comments_on_articles()
        self = self.users_with_count_marks_on_articles()
        self = self.users_with_date_latest_article()

        return self


class UserMarkQuerySet(NullsLastQuerySet):
    """

    """

    def users_with_total_count_marks(self):

        return self.annotate(total_count_marks=models.Count('marks', distinct=True))

    def users_with_date_latest_mark(self):

        return self.annotate(date_latest_mark=models.Max('marks__created'))

    def users_with_count_marks_and_latest_mark(self):

        self = self.users_with_total_count_marks()
        self = self.users_with_date_latest_mark()

        return self
