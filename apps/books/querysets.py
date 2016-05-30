
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

        return self.annotate(rating=models.Avg('scopes__scope'))

    def books_with_count_tags_links_replies_and_rating(self):
        """Complex queryset with count tags, links, replies and rating of each the book."""

        return self.books_with_count_tags().books_with_count_links().\
            books_with_count_replies().books_with_rating()

    def new_books(self):
        """Books published no later in this and past year."""

        return self.filter(year_published__gte=NOW_YEAR - 1).filter(year_published__lte=NOW_YEAR)
