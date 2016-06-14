
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
        used_lexers = self.values_list('lexer', flat=True)
        counter_used_lexers = collections.Counter(used_lexers).most_common()
        do_not_used_lexers = tuple((code, 0) for code, name in self.model.CHOICES_LEXERS if code not in itertools.chain.from_iterable(counter_used_lexers))
        counter_lexers = list(counter_used_lexers) + list(do_not_used_lexers)
        return counter_lexers

    # tuple(filter(lambda x: x[0] == 'yaml', Snippet.CHOICES_LEXERS))
    #  may be need flat list counter_used_lexers for chech IN
