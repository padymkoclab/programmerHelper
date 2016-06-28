
import itertools
import collections

from django.utils import timezone
from django.db import models

from dateutil.relativedelta import relativedelta

from apps.tags.models import Tag


class SnippetManager(models.Manager):
    """
    Model manager for snippets.
    """

    def change_lexer_of_snippet(self, snippet, lexer):
        """Change lexer of snippet."""

        snippet.lexer = lexer
        snippet.full_clean()
        snippet.save()

    def make_snippet_as_pythonic(self, snippet):
        """Set lexer python for snippet."""

        self.change_lexer_of_snippet(snippet=snippet, lexer='python3')

    def get_statistics_by_usage_all_lexers(self):
        """Getting a statistics by total usage of each a lexer on all a snippets."""

        # found and count used lexers
        used_lexers = self.values_list('lexer', flat=True)
        counter_used_lexers = collections.Counter(used_lexers).most_common()

        # got codes of used lexer to find non used lexers
        codes_used_lexers = tuple(itertools.chain.from_iterable(counter_used_lexers))
        do_not_used_lexers = ((code, 0) for code, name in self.model.CHOICES_LEXERS if code not in codes_used_lexers)

        # contate counters used and don`t used lexers
        counter_lexers = list(counter_used_lexers) + list(do_not_used_lexers)

        #
        result = list()
        for code_lexer, value in counter_lexers:
            for code_lexer2, display_lexer_name in self.model.CHOICES_LEXERS:
                if code_lexer2 == code_lexer:
                    result.append((display_lexer_name, value))

        return tuple(result)

    def get_statistics_by_usage_tags(self):
        """Getting a statistics by total usage of each a tag on all a snippets."""

        # get primary keys a tags used in all a snippets
        pks_used_tags = self.values_list('tags__pk', flat=True)

        # counter primary keys the tags
        counter_used_tags = collections.Counter(pks_used_tags).most_common()

        # replace primary key of each the tag on itself object
        counter_used_tags = tuple(
            (Tag.objects.get(pk=tag_pk), count_usage_tag) for tag_pk, count_usage_tag in counter_used_tags
        )

        return counter_used_tags

    def get_statistics_count_snippets_by_months_for_past_year(self):
        """Get statistics by count snippets for past year."""

        now = timezone.now()
        result = list()
        for month in range(13, 0, -1):
            datetime_ago = now - relativedelta(months=month)
            count_snippets = self.filter(
                date_added__month__lte=datetime_ago.month,
                date_added__year__lte=datetime_ago.year
            ).count()
            result.append(((datetime_ago.year, datetime_ago.month), count_snippets))
        return result


class PythonSnippetManager(models.Manager):

    def get_queryset(self):
        return super(PythonSnippetManager, self).get_queryset().filter(lexer='python')
