
from django.test import TestCase

from apps.accounts.factories import accounts_factory
from apps.tags.factories import tags_factory
from apps.tags.models import Tag
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
        tags_factory()

    def test_change_lexer_of_snippet(self):
        # create new snippet
        snippet = SnippetFactory(lexer='awk')
        self.assertEqual(snippet.lexer, 'awk')
        # change lexer of snippet
        Snippet.objects.change_lexer_of_snippet(snippet, 'bash')
        snippet.refresh_from_db()
        self.assertEqual(snippet.lexer, 'bash')

    def test_make_snippet_as_pythonic(self):
        # create new snippet
        snippet = SnippetFactory(lexer='css')
        self.assertEqual(snippet.lexer, 'css')
        # made snippet as pythonic
        Snippet.objects.make_snippet_as_pythonic(snippet)
        snippet.refresh_from_db()
        self.assertEqual(snippet.lexer, 'python3')

    def test_get_statistics_by_usage_all_lexers(self):

        # Dictionary with key as code of lexer and values - count snippets with this lexer.
        lexers_with_count_using = {
            'bash': 6,
            'css': 7,
            'django_jinja': 1,
            'html': 9,
            'html_django_jinja': 8,
            'ipython3': 2,
            'javascript': 11,
            'javascript_django_jinja': 2,
            'json': 4,
            'mysql': 3,
            'numpy': 3,
            'postgresql_console': 5,
            'python3': 12,
            'restructuredtext': 1,
            'sql': 3,
            'xml': 2,
            'yaml': 3,
        }

        # create snippets with lexers
        for lexer, count in lexers_with_count_using.items():
            for i in range(count):
                snippet = SnippetFactory(lexer=lexer)
                snippet.full_clean()

        # checkup
        statistics_by_lexers = Snippet.objects.get_statistics_by_usage_all_lexers()
        self.assertSequenceEqual(statistics_by_lexers[:8], (
            ('Python', 12),
            ('JavaScript', 11),
            ('HTML', 9),
            ('HTML+Django/Jinja', 8),
            ('CSS', 7),
            ('Bash', 6),
            ('PostgreSQL', 5),
            ('JSON', 4),
        ))
        self.assertCountEqual(statistics_by_lexers[8:12], (
            ('YAML', 3),
            ('SQL', 3),
            ('NumPy', 3),
            ('MySQL', 3),
        ))
        self.assertCountEqual(statistics_by_lexers[12:15], (
            ('XML', 2),
            ('IPython', 2),
            ('JavaScript+Django/Jinja', 2),
        ))
        self.assertCountEqual(statistics_by_lexers[15:17], (
            ('reStructuredText', 1),
            ('Django/Jinja', 1),
        ))
        self.assertCountEqual(statistics_by_lexers[17:], (
            ('CSS+Django/Jinja', 0),
            ('Awk', 0),
            ('CoffeeScript', 0),
        ))

    def test_get_statistics_by_usage_tags(self):
        self.assertSequenceEqual(Snippet.objects.get_statistics_by_usage_tags(), ())
        #
        tag_python = Tag.objects.get(name='python')
        tag_django = Tag.objects.get(name='django')
        tag_jquery = Tag.objects.get(name='jqueryjs')
        tag_javascript = Tag.objects.get(name='javascript')
        tag_linux = Tag.objects.get(name='linux')
        tag_bootstrap = Tag.objects.get(name='bootstrap')
        tag_angularjs = Tag.objects.get(name='angularjs')
        tag_backbonejs = Tag.objects.get(name='backbonejs')
        tag_html = Tag.objects.get(name='html')
        # not used tag
        Tag.objects.get(name='css')
        #
        snippet = SnippetFactory()
        snippet.tags.set([tag_python])
        self.assertSequenceEqual(
            Snippet.objects.get_statistics_by_usage_tags(),
            ((tag_python, 1), )
        )
        #
        snippet = SnippetFactory()
        snippet.tags.set([tag_python, tag_javascript, tag_angularjs, tag_django])
        statistics_by_usage_tags = Snippet.objects.get_statistics_by_usage_tags()
        self.assertSequenceEqual(
            statistics_by_usage_tags[0],
            (tag_python, 2)
        )
        self.assertCountEqual(
            statistics_by_usage_tags[1:],
            ((tag_javascript, 1), (tag_angularjs, 1), (tag_django, 1))
        )
        #
        snippet = SnippetFactory()
        snippet.tags.set([tag_angularjs, tag_javascript, tag_linux, tag_backbonejs, tag_django])
        statistics_by_usage_tags = Snippet.objects.get_statistics_by_usage_tags()
        self.assertCountEqual(
            statistics_by_usage_tags[:4],
            ((tag_python, 2), (tag_django, 2), (tag_javascript, 2), (tag_angularjs, 2))
        )
        self.assertCountEqual(
            statistics_by_usage_tags[4:],
            ((tag_linux, 1), (tag_backbonejs, 1))
        )
        #
        snippet = SnippetFactory()
        snippet.tags.set([tag_python, tag_django, tag_html, tag_jquery, tag_bootstrap, tag_linux])
        statistics_by_usage_tags = Snippet.objects.get_statistics_by_usage_tags()
        self.assertCountEqual(
            statistics_by_usage_tags[:2],
            ((tag_python, 3), (tag_django, 3))
        )
        self.assertCountEqual(
            statistics_by_usage_tags[2:5],
            ((tag_linux, 2), (tag_javascript, 2), (tag_angularjs, 2))
        )
        self.assertCountEqual(
            statistics_by_usage_tags[5:],
            ((tag_bootstrap, 1), (tag_backbonejs, 1), (tag_html, 1), (tag_jquery, 1))
        )
        #
        snippet = SnippetFactory()
        snippet.tags.set([tag_jquery, tag_django, tag_bootstrap, tag_python, tag_javascript, tag_linux])
        statistics_by_usage_tags = Snippet.objects.get_statistics_by_usage_tags()
        self.assertCountEqual(
            statistics_by_usage_tags[:2],
            ((tag_python, 4), (tag_django, 4))
        )
        self.assertCountEqual(
            statistics_by_usage_tags[2:4],
            ((tag_linux, 3), (tag_javascript, 3))
        )
        self.assertCountEqual(
            statistics_by_usage_tags[4:-2],
            ((tag_jquery, 2), (tag_angularjs, 2), (tag_bootstrap, 2))
        )
        self.assertCountEqual(
            statistics_by_usage_tags[-2:],
            ((tag_html, 1), (tag_backbonejs, 1))
        )
        #
        snippet = SnippetFactory()
        snippet.tags.set([tag_jquery, tag_bootstrap, tag_python, tag_backbonejs])
        statistics_by_usage_tags = Snippet.objects.get_statistics_by_usage_tags()
        self.assertSequenceEqual(
            statistics_by_usage_tags[:2],
            ((tag_python, 5), (tag_django, 4))
        )
        self.assertCountEqual(
            statistics_by_usage_tags[2:6],
            ((tag_linux, 3), (tag_javascript, 3), (tag_jquery, 3), (tag_bootstrap, 3))
        )
        self.assertCountEqual(
            statistics_by_usage_tags[6:8],
            ((tag_backbonejs, 2), (tag_angularjs, 2))
        )
        self.assertCountEqual(
            statistics_by_usage_tags[-1],
            (tag_html, 1)
        )
