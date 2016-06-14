
from django.test import TestCase

from apps.accounts.factories import accounts_factory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory

from apps.snippets.factories import SnippetFactory
from apps.snippets.models import Snippet


class SnippetManagerTest(TestCase):
    """
    Tests for managers of the model of snippets.
    """

    @classmethod
    def setUpTestData(cls):
        badges_factory()
        accounts_factory(20)
        tags_factory(10)

    def test_change_lexer_of_snippet(self):
        # create new snippet
        snippet = SnippetFactory(lexer='awk')
        self.assertEqual(snippet.lexer, 'awk')
        # change lexer of snippet
        Snippet.objects.change_lexer_of_snippet(snippet, 'java')
        snippet.refresh_from_db()
        self.assertEqual(snippet.lexer, 'java')

    def test_make_snippet_as_pythonic(self):
        # create new snippet
        snippet = SnippetFactory(lexer='ruby')
        self.assertEqual(snippet.lexer, 'ruby')
        # made snippet as pythonic
        Snippet.objects.make_snippet_as_pythonic(snippet)
        snippet.refresh_from_db()
        self.assertEqual(snippet.lexer, 'python3')

    def test_give_statistics_by_lexers(self):

        # Dictionary with key as code of lexer and values - count snippets with this lexer.
        lexers_with_count_using = {
            'awk': 1,
            'base_makefile': 0,
            'bash': 6,
            'coffescript': 1,
            'css': 7,
            'css_django_jinja': 4,
            'css_php': 0,
            'css_ruby': 0,
            'django_jinja': 1,
            'html': 9,
            'html_django_jinja': 8,
            'html_php': 0,
            'ipython3': 2,
            'java': 0,
            'javascript': 11,
            'javascript_django_jinja': 2,
            'javascript_php': 0,
            'javascript_ruby': 0,
            'json': 4,
            'lesscss': 0,
            'makefile': 1,
            'mysql': 3,
            'numpy': 3,
            'perl': 0,
            'perl6': 0,
            'php': 0,
            'postgresql': 5,
            'python2': 2,
            'python3': 12,
            'restructuredtext': 1,
            'ruby': 0,
            'sass': 0,
            'scala': 0,
            'scss': 0,
            'sql': 3,
            'xml': 2,
            'yaml': 3,
        }

        # create snippets with lexers
        for lexer, count in lexers_with_count_using.items():
            for i in range(count):
                SnippetFactory(lexer=lexer)

        # checkup
        statistics_by_lexers = Snippet.objects.give_statistics_by_lexers()
        self.assertSequenceEqual(statistics_by_lexers[:7], (
            ('python3', 12),
            ('javascript', 11),
            ('html', 9),
            ('html_django_jinja', 8),
            ('css', 7),
            ('bash', 6),
            ('postgresql', 5),
        ))
        self.assertCountEqual(statistics_by_lexers[7:9], (
            ('json', 4),
            ('css_django_jinja', 4),
        ))
        self.assertCountEqual(statistics_by_lexers[9:13], (
            ('yaml', 3),
            ('sql', 3),
            ('numpy', 3),
            ('mysql', 3),
        ))
        self.assertCountEqual(statistics_by_lexers[13:17], (
            ('python2', 2),
            ('xml', 2),
            ('ipython3', 2),
            ('javascript_django_jinja', 2),
        ))
        self.assertCountEqual(statistics_by_lexers[17:22], (
            ('restructuredtext', 1),
            ('makefile', 1),
            ('django_jinja', 1),
            ('awk', 1),
            ('coffescript', 1),
        ))
        self.assertCountEqual(statistics_by_lexers[22:], (
            ('ruby', 0),
            ('sass', 0),
            ('scala', 0),
            ('java', 0),
            ('html_php', 0),
            ('scss', 0),
            ('perl', 0),
            ('perl6', 0),
            ('php', 0),
            ('lesscss', 0),
            ('javascript_php', 0),
            ('javascript_ruby', 0),
            ('css_php', 0),
            ('css_ruby', 0),
            ('base_makefile', 0),
            ('postgresql_console', 0),
        ))
