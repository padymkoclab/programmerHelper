
import itertools
import collections

from django.db import models


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

    def give_statistics_by_lexers(self):
        # found and count used lexers
        used_lexers = self.values_list('lexer', flat=True)
        counter_used_lexers = collections.Counter(used_lexers).most_common()

        # got codes of used lexer to find non used lexers
        codes_used_lexers = tuple(itertools.chain.from_iterable(counter_used_lexers))
        do_not_used_lexers = ((code, 0) for code, name in self.model.CHOICES_LEXERS if code not in codes_used_lexers)

        # contate adn return counters used and don`t used lexers
        counter_lexers = list(counter_used_lexers) + list(do_not_used_lexers)
        return counter_lexers
