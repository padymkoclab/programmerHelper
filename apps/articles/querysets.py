
import numbers

from django.utils import timezone
from django.db import models

from mylabour.functions_db import Round


class ArticleQuerySet(models.QuerySet):
    """
    Suit methods for work with queryset of artices.
    """

    def articles_with_rating(self):
        """Adding for each the article field with determined rating of an itself."""

        self = self.defer('subsections').annotate(rating=models.Avg('scopes__scope'))
        self = self.annotate(rating=models.functions.Coalesce('rating', .0))
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

        return self.defer('subsections').annotate(count_comments=models.Count('comments', distinct=True))

    def articles_with_count_scopes(self):
        """Adding for each the article field with determined count scopes of an itself."""

        return self.defer('scopes').annotate(count_scopes=models.Count('scopes', distinct=True))

    def articles_with_count_tags(self):
        """Adding for each the article field with determined count tags of an itself."""

        return self.defer('subsections').annotate(count_tags=models.Count('tags', distinct=True))

    def articles_with_count_links(self):
        """Adding for each the article field with determined count useful links, used in each article."""

        return self.defer('subsections').annotate(count_links=models.Count('links', distinct=True))

    def articles_with_count_subsections(self):
        """Adding for each the article field with determined count subsections of an itself."""

        return self.defer('subsections').annotate(count_subsections=models.Count('subsections', distinct=True))

    def articles_with_rating_and_count_comments_subsections_tags_links_scopes(self):
        """Determining for each article: count tags, comments, links, scopes, subsections and rating."""

        self = self.articles_with_rating()
        self = self.articles_with_count_comments()
        self = self.articles_with_count_scopes()
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

        return self.only('date_added').filter(date_added__range=[timezone.now() - timezone.timedelta(weeks=1), timezone.now()])

    def articles_from_external_resourse(self):
        """Articles from external resourse pinted in field 'source'."""

        return self.only('sourse').filter(source__isnull=False)

    def own_articles(self):
        """Own articles, published from website`s authors."""

        return self.only('sourse').filter(source__isnull=True)

    def hot_articles(self):
        """Articles with 7 and more comments."""

        articles_with_count_comments = self.articles_with_count_comments()
        return articles_with_count_comments.filter(count_comments__gte=7)

    def popular_articles(self):
        """Articles with rating from 4 and more."""

        self = self.articles_with_rating()
        return self.filter(rating__gte=4)

    def articles_by_rating(self, min_rating=None, max_rating=None):
        """Filter articles by certain range of rating."""

        if min_rating is None and max_rating is None:
            raise AttributeError('Please point at least either min_rating or max_rating.')
        self = self.articles_with_rating()
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
