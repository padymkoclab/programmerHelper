
import string
import re
import unittest
import datetime
import sys

sys.path = [
    '',
    '/home/wlysenko/.virtualenvs/virtual_programmerHelper/project_programmerHelper',
    '/home/wlysenko/.virtualenvs/virtual_programmerHelper/lib/python3.4',
    '/home/wlysenko/.virtualenvs/virtual_programmerHelper/lib/python3.4/plat-x86_64-linux-gnu',
    '/home/wlysenko/.virtualenvs/virtual_programmerHelper/lib/python3.4/lib-dynload',
    '/usr/lib/python3.4',
    '/usr/lib/python3.4/plat-x86_64-linux-gnu',
    '/home/wlysenko/.virtualenvs/virtual_programmerHelper/lib/python3.4/site-packages',
    '/home/wlysenko/.virtualenvs/virtual_programmerHelper/lib/python3.4/site-packages/IPython/extensions',
    '/home/wlysenko/.ipython'
]

import django
from django.conf import settings

settings.configure()
django.setup()

from mylabour import utils
from mylabour.constants import RUSSIAN_LETTERS


# @unittest.skip('reason')
class TestUtils_get_different_between_elements(unittest.TestCase):
    """

    """

    def setUp(self):
        self.sequence_with_integer = [67, 13, 52, 64, -92, 4, -47, 17, 71, 95]
        self.sequence_with_dates = [
            datetime.date(2016, 11, 11),
            datetime.date(2016, 7, 6),
            datetime.date(2016, 1, 24),
            datetime.date(2014, 4, 6),
            datetime.date(2011, 7, 15),
            datetime.date(2014, 8, 3),
            datetime.date(2000, 4, 15),
            datetime.date(2006, 7, 7),
        ]

    def tearDown(self):
        del self.sequence_with_integer
        del self.sequence_with_dates

    def test_get_different_between_elements_with_integer(self):
        self.assertSequenceEqual(
            utils.get_different_between_elements(self.sequence_with_integer, left_to_right=True),
            [54, -39, -12, 156, -96, 51, -64, -54, -24],
        )
        self.assertSequenceEqual(
            utils.get_different_between_elements(self.sequence_with_integer, left_to_right=False),
            [-54, 39, 12, -156, 96, -51, 64, 54, 24],
        )

    def test_get_different_between_elements_with_dates(self):
        self.assertSequenceEqual(
            utils.get_different_between_elements(self.sequence_with_dates, left_to_right=True),
            list(datetime.timedelta(i) for i in (128, 164, 658, 996, -1115, 5223, -2274)),
        )
        self.assertSequenceEqual(
            utils.get_different_between_elements(self.sequence_with_dates, left_to_right=False),
            list(datetime.timedelta(i) for i in (-128, -164, -658, -996, 1115, -5223, 2274)),
        )


# @unittest.skip('reason')
class TestUtils_show_concecutive_certain_element(unittest.TestCase):
    """

    """

    def setUp(self):
        self.sequence1 = [1, 2, 1, 1, 1, 1, 1, 3, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1]
        self.sequence2 = [2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1]

    def tearDown(self):
        del self.sequence1
        del self.sequence2

    def test_show_concecutive_certain_element(self):
        self.assertSequenceEqual(
            utils.show_concecutive_certain_element(self.sequence1, element=1),
            [[1], [1, 1, 1, 1, 1], [1, 1], [1, 1], [1, 1], [1, 1, 1]],
        )
        self.assertSequenceEqual(
            utils.show_concecutive_certain_element(self.sequence2, element=1),
            [[1], [1], [1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1]],
        )


# @unittest.skip('reason')
class GenerateTextByMinLengthTest(unittest.TestCase):
    """
    Test for function utils.generate_text_by_min_length.
    """

    def test_length_returned_text(self):
        """Length generated text must be equal or more than determined."""

        for i in range(1, 1000):
            text = utils.generate_text_by_min_length(i)
            self.assertGreaterEqual(len(text), i)

    def test_text_ending(self):
        """Text must be ending on point, question mark or exclamation mark."""

        for i in range(1, 1000):
            text = utils.generate_text_by_min_length(i)
            self.assertIn(text[-1], ['.', '!', '?'])

    def test_text_may_contains(self):
        """Text may constains letters, space, comma, point, question mark, exclamation mark ann double break for paragraph"""

        for i in range(1, 1000):
            text = utils.generate_text_by_min_length(i)
            # remove !,. ?, leave only letters
            text = re.sub('[!?., \n]', '', text)
            if not text.isalpha():
                print(text.__repr__())
            self.assertTrue(text.isalpha())

    def test_text_contains_not_numners(self):
        """Text must contains not numbers."""

        pattern = re.compile(r'\d+')
        for i in range(1, 1000):
            text = utils.generate_text_by_min_length(i)
            self.assertFalse(re.search(pattern, text))

    def test_text_as_html_paragraphs(self):
        for i in range(1, 1000):
            text = utils.generate_text_by_min_length(i, as_p=True)
            self.assertEqual(text[:3], '<p>')
            self.assertEqual(text[-4:], '</p>')


# @unittest.skip('reason')
class FindAllWordsTest(unittest.TestCase):
    """
    Tests for method utils.findall_words
    """

    def test_return_if_text_if_empty(self):
        text = ''
        words = utils.findall_words(text)
        self.assertEqual(words, [])

    def test_return_word_from_single_word_text(self):
        text = 'bytes-like'
        words = utils.findall_words(text)
        self.assertSequenceEqual(words, ['bytes-like'])

    def test_return_words_from_tiny_text(self):
        text = 'For locally defined plug-ins I prefer to rely on explicit conftest.py declarations:'
        words = utils.findall_words(text)
        self.assertSequenceEqual(words, [
            'For', 'locally', 'defined', 'plug-ins', 'I', 'prefer', 'to',
            'rely', 'on', 'explicit', 'conftest.py', 'declarations'
        ])
        text = 'For example, BufferedIOBase provides unoptimized implementations of readinto() and readline().'
        words = utils.findall_words(text)
        self.assertSequenceEqual(words, [
            'For', 'example', 'BufferedIOBase', 'provides', 'unoptimized', 'implementations',
            'of', 'readinto', 'and', 'readline',
        ])

    def test_return_words_from_small_text(self):
        text = 'Add the option to filter by a custom date range on the admin. This allows\
        to inputs to be used to get the custom date range filters.'
        words = utils.findall_words(text)
        self.assertSequenceEqual(words, [
            'Add', 'the', 'option', 'to', 'filter', 'by', 'a', 'custom', 'date',
            'range', 'on', 'the', 'admin', 'This', 'allows', 'to', 'inputs', 'to',
            'be', 'used', 'to', 'get', 'the', 'custom', 'date', 'range', 'filters'
        ])

    def test_return_words_from_big_text(self):
        text = """If you want to use pytest instead of Django's test runner and also get the \
        power of function-based tests, fixture functions, improved test discover, and all the \
        stuff I haven't covered, then check out and/or pip install pytest-django. My admittedly \
        brief usage on some of my existing projects has demonstrating that my existing \
        unittest-style tests work.

        That previous tests still function means that as with a pure Python project, I can rely \
        on existing unittests and write all my new tests as functions. I guess I could say that \
        my existing Django projects just got much easier to maintain.

        A good example of using pytest with Django can be found in django-braces tox.ini file."""
        words = utils.findall_words(text)
        self.assertSequenceEqual(words, [
            'If', 'you', 'want', 'to', 'use', 'pytest', 'instead', 'of', "Django's", 'test', 'runner',
            'and', 'also', 'get', 'the', 'power', 'of', 'function-based', 'tests', 'fixture',
            'functions', 'improved', 'test', 'discover', 'and', 'all', 'the', 'stuff', 'I', "haven't",
            'covered', 'then', 'check', 'out', 'and', 'or', 'pip', 'install', 'pytest-django', 'My',
            'admittedly', 'brief', 'usage', 'on', 'some', 'of', 'my', 'existing', 'projects', 'has',
            'demonstrating', 'that', 'my', 'existing', 'unittest-style', 'tests', 'work', 'That',
            'previous', 'tests', 'still', 'function', 'means', 'that', 'as', 'with', 'a', 'pure',
            'Python', 'project', 'I', 'can', 'rely', 'on', 'existing', 'unittests', 'and', 'write',
            'all', 'my', 'new', 'tests', 'as', 'functions', 'I', 'guess', 'I', 'could', 'say', 'that',
            'my', 'existing', 'Django', 'projects', 'just', 'got', 'much', 'easier', 'to', 'maintain',
            'A', 'good', 'example', 'of', 'using', 'pytest', 'with', 'Django', 'can', 'be', 'found',
            'in', "django-braces", 'tox.ini', 'file'
        ])

    def test_return_words_from_vast_text(self):
        text = """Introduction

        Django is a powerful web framework that can help you get your Python application or \
        website off the ground. Django includes a simplified development server for testing \
        your code locally, but for anything even slightly production related, a more secure \
        and powerful web server is required.

        In this guide, we will demonstrate how to install and configure some components on \
        Ubuntu 14.04 to support and serve Django applications. We will be setting up a \
        PostgreSQL database instead of using the default SQLite database. We will configure \
        the Gunicorn application server to interface with our applications. We will then set \
        up Nginx to reverse proxy to Gunicorn, giving us access to its security and performance \
        features to serve our apps.

        Prerequisites and Goals

        In order to complete this guide, you should have a fresh Ubuntu 14.04 server instance \
        with a non-root user with sudo privileges configured. You can learn how to set this up \
        by running through our initial server setup guide.

        We will be installing Django within a virtual environment. Installing Django into an \
        environment specific to your project will allow your projects and their requirements \
        to be handled separately.

        Once we have our database and application up and running, we will install and configure \
        the Gunicorn application server. This will serve as an interface to our application, \
        translating client requests in HTTP to Python calls that our application can process. \
        We will then set up Nginx in front of Gunicorn to take advantage of its high performance \
        connection handling mechanisms and its easy-to-implement security features.

        Let's get started.
        Since we already have a project directory, we will tell Django to install the files \
        here. It will create a second level directory with the actual code, which is normal, \
        and place a management script in this directory. The key to this is the dot at the \
        end that tells Django to create the files in the current directory:
        Change the settings with your PostgreSQL database information. We tell Django to use \
        the psycopg2 adaptor we installed with pip. We need to give the database name, the \
        database username, the database username's password, and then specify that the database \
        is located on the local computer. You can leave the PORT setting as an empty string:
        In this guide, we've set up a Django project in its own virtual environment. We've \
        configured Gunicorn to translate client requests so that Django can handle them. \
        Afterwards, we set up Nginx to act as a reverse proxy to handle client connections \
        and serve the correct project depending on the client request.

        Django makes creating projects and applications simple by providing many of the common \
        pieces, allowing you to focus on the unique elements. By leveraging the general tool \
        chain described in this article, you can easily serve the applications you create from \
        a single serve.
        """
        words = utils.findall_words(text)
        self.assertSequenceEqual(words, [
            'Introduction', 'Django', 'is', 'a', 'powerful', 'web', 'framework', 'that', 'can', 'help',
            'you', 'get', 'your', 'Python', 'application', 'or', 'website', 'off', 'the', 'ground',
            'Django', 'includes', 'a', 'simplified', 'development', 'server', 'for', 'testing', 'your', 'code',
            'locally', 'but', 'for', 'anything', 'even', 'slightly', 'production', 'related', 'a', 'more',
            'secure', 'and', 'powerful', 'web', 'server', 'is', 'required', 'In', 'this', 'guide',
            'we', 'will', 'demonstrate', 'how', 'to', 'install', 'and', 'configure', 'some', 'components',
            'on', 'Ubuntu', '14.04', 'to', 'support', 'and', 'serve', 'Django', 'applications', 'We',
            'will', 'be', 'setting', 'up', 'a', 'PostgreSQL', 'database', 'instead', 'of', 'using',
            'the', 'default', 'SQLite', 'database', 'We', 'will', 'configure', 'the', 'Gunicorn', 'application',
            'server', 'to', 'interface', 'with', 'our', 'applications', 'We', 'will', 'then', 'set',
            'up', 'Nginx', 'to', 'reverse', 'proxy', 'to', 'Gunicorn', 'giving', 'us', 'access',
            'to', 'its', 'security', 'and', 'performance', 'features', 'to', 'serve', 'our', 'apps',
            'Prerequisites', 'and', 'Goals', 'In', 'order', 'to', 'complete', 'this', 'guide', 'you',
            'should', 'have', 'a', 'fresh', 'Ubuntu', '14.04', 'server', 'instance', 'with', 'a',
            'non-root', 'user', 'with', 'sudo', 'privileges', 'configured', 'You', 'can', 'learn', 'how',
            'to', 'set', 'this', 'up', 'by', 'running', 'through', 'our', 'initial', 'server',
            'setup', 'guide', 'We', 'will', 'be', 'installing', 'Django', 'within', 'a', 'virtual',
            'environment', 'Installing', 'Django', 'into', 'an', 'environment', 'specific', 'to', 'your', 'project',
            'will', 'allow', 'your', 'projects', 'and', 'their', 'requirements', 'to', 'be', 'handled',
            'separately', 'Once', 'we', 'have', 'our', 'database', 'and', 'application', 'up', 'and',
            'running', 'we', 'will', 'install', 'and', 'configure', 'the', 'Gunicorn', 'application', 'server',
            'This', 'will', 'serve', 'as', 'an', 'interface', 'to', 'our', 'application', 'translating',
            'client', 'requests', 'in', 'HTTP', 'to', 'Python', 'calls', 'that', 'our', 'application',
            'can', 'process', 'We', 'will', 'then', 'set', 'up', 'Nginx', 'in', 'front',
            'of', 'Gunicorn', 'to', 'take', 'advantage', 'of', 'its', 'high', 'performance', 'connection',
            'handling', 'mechanisms', 'and', 'its', 'easy-to-implement', 'security', 'features', "Let's", 'get', 'started',
            'Since', 'we', 'already', 'have', 'a', 'project', 'directory', 'we', 'will', 'tell',
            'Django', 'to', 'install', 'the', 'files', 'here', 'It', 'will', 'create', 'a',
            'second', 'level', 'directory', 'with', 'the', 'actual', 'code', 'which', 'is', 'normal',
            'and', 'place', 'a', 'management', 'script', 'in', 'this', 'directory', 'The', 'key',
            'to', 'this', 'is', 'the', 'dot', 'at', 'the', 'end', 'that', 'tells',
            'Django', 'to', 'create', 'the', 'files', 'in', 'the', 'current', 'directory', 'Change',
            'the', 'settings', 'with', 'your', 'PostgreSQL', 'database', 'information', 'We', 'tell', 'Django',
            'to', 'use', 'the', 'psycopg2', 'adaptor', 'we', 'installed', 'with', 'pip', 'We',
            'need', 'to', 'give', 'the', 'database', 'name', 'the', 'database', 'username', 'the',
            'database', "username's", 'password', 'and', 'then', 'specify', 'that', 'the', 'database', 'is',
            'located', 'on', 'the', 'local', 'computer', 'You', 'can', 'leave', 'the', 'PORT',
            'setting', 'as', 'an', 'empty', 'string', 'In', 'this', 'guide', "we've", 'set',
            'up', 'a', 'Django', 'project', 'in', 'its', 'own', 'virtual', 'environment', "We've",
            'configured', 'Gunicorn', 'to', 'translate', 'client', 'requests', 'so', 'that', 'Django', 'can',
            'handle', 'them', 'Afterwards', 'we', 'set', 'up', 'Nginx', 'to', 'act', 'as',
            'a', 'reverse', 'proxy', 'to', 'handle', 'client', 'connections', 'and', 'serve', 'the',
            'correct', 'project', 'depending', 'on', 'the', 'client', 'request', 'Django', 'makes', 'creating',
            'projects', 'and', 'applications', 'simple', 'by', 'providing', 'many', 'of', 'the', 'common',
            'pieces', 'allowing', 'you', 'to', 'focus', 'on', 'the', 'unique', 'elements', 'By',
            'leveraging', 'the', 'general', 'tool', 'chain', 'described', 'in', 'this', 'article', 'you',
            'can', 'easily', 'serve', 'the', 'applications', 'you', 'create', 'from', 'a', 'single', 'serve'
        ])

    def test_return_word_in_very_polute_text(self):
        text = '###At***the!!end @@of#a@so-called \'age&of%-%peace\' %, \
        two$$great^^nations??of!immortals##march (against) ++``each~|| ~other.'
        words = utils.findall_words(text)
        self.assertSequenceEqual(words, [
            'At', 'the', 'end', 'of', 'a', 'so-called', 'age', 'of', 'peace', 'two',
            'great', 'nations', 'of', 'immortals', 'march', 'against', 'each', 'other',
        ])

    def test_validation_input_as_string(self):
        self.assertRaises(TypeError, utils.findall_words, float())
        self.assertRaises(TypeError, utils.findall_words, int())
        self.assertRaises(TypeError, utils.findall_words, list())
        self.assertRaises(TypeError, utils.findall_words, set())
        utils.findall_words('')


# @unittest.skip('reason')
class GenerateWordsTest(unittest.TestCase):
    """
    Tests for utils.generate_words_separated_commas
    """

    def test_accepted_only_integer_as_limiters_count_words(self):
        self.assertRaisesRegex(ValueError, 'must be integer', utils.generate_words, min_count_words=1.1, max_count_words=3)
        self.assertRaisesRegex(ValueError, 'must be integer', utils.generate_words, min_count_words=1.1, max_count_words=3.1)
        self.assertRaisesRegex(ValueError, 'must be integer', utils.generate_words, min_count_words=None, max_count_words=3)
        self.assertRaisesRegex(ValueError, 'must be integer', utils.generate_words, min_count_words='1', max_count_words=10)

    def test_if_min_limiter_is_great_than_max_limiter(self):
        self.assertRaisesRegex(ValueError, 'must be not great than', utils.generate_words, min_count_words=1, max_count_words=0)
        self.assertRaisesRegex(ValueError, 'must be not great than', utils.generate_words, min_count_words=10, max_count_words=-1)
        self.assertRaisesRegex(ValueError, 'must be not great than', utils.generate_words, min_count_words=11, max_count_words=-1)
        self.assertRaisesRegex(ValueError, 'must be not great than', utils.generate_words, min_count_words=11, max_count_words=10)

    def test_if_min_limiter_or_max_limiter_is_less_1(self):
        self.assertRaisesRegex(ValueError, 'must be 1 or more', utils.generate_words, min_count_words=0, max_count_words=0)
        self.assertRaisesRegex(ValueError, 'must be 1 or more', utils.generate_words, min_count_words=0, max_count_words=1)

    def test_restrict_value_register_of_words(self):
        self.assertRaisesRegex(
            ValueError,
            "must be 'capitalize', 'lower', 'title' or 'upper'",
            utils.generate_words,
            min_count_words=1, max_count_words=1, to_register='swap'
        )
        self.assertRaisesRegex(
            ValueError,
            "must be 'capitalize', 'lower', 'title' or 'upper'",
            utils.generate_words,
            min_count_words=1, max_count_words=1, to_register=''
        )
        self.assertRaisesRegex(
            ValueError,
            "must be 'capitalize', 'lower', 'title' or 'upper'",
            utils.generate_words,
            min_count_words=1, max_count_words=1, to_register=int
        )

    def test_restrict_locale_of_words(self):
        self.assertRaisesRegex(
            ValueError, "('en' or 'ru')", utils.generate_words, min_count_words=1, max_count_words=1, locale='uk'
        )
        self.assertRaisesRegex(
            ValueError, "('en' or 'ru')", utils.generate_words, min_count_words=1, max_count_words=1, locale=float()
        )
        self.assertRaisesRegex(
            ValueError, "('en' or 'ru')", utils.generate_words, min_count_words=1, max_count_words=1, locale='fr'
        )

    def test_count_words(self):
        words = utils.generate_words(min_count_words=1, max_count_words=100)
        self.assertIn(len(words), range(1, 100 + 1))
        words = utils.generate_words(min_count_words=1, max_count_words=1)
        self.assertEqual(len(words), 1)
        words = utils.generate_words(min_count_words=1, max_count_words=2)
        self.assertIn(len(words), [1, 2])
        words = utils.generate_words(min_count_words=55, max_count_words=55)
        self.assertEqual(len(words), 55)
        words = utils.generate_words(min_count_words=1000, max_count_words=3000)
        self.assertIn(len(words), range(1000, 3000 + 1))

    def test_random_count_words(self):
        counter_count_words = set()
        for i in range(100):
            count_words = len(utils.generate_words(min_count_words=1, max_count_words=10))
            counter_count_words.add(count_words)
        self.assertGreater(len(counter_count_words), 7)

    def test_returned_words_contains_only_letters(self):
        words = utils.generate_words(min_count_words=30, max_count_words=40)
        for word in words:
            self.assertTrue(word.isalpha())

    def test_locale_words(self):
        # english
        words = utils.generate_words(min_count_words=25, max_count_words=30, locale='en')
        for word in words:
            self.assertTrue(all((char in string.ascii_letters for char in word)))
        # russian
        words = utils.generate_words(min_count_words=25, max_count_words=30, locale='ru')
        for word in words:
            self.assertTrue(all((char in RUSSIAN_LETTERS for char in word)))

    def test_register_words(self):
        # capitalize
        words = utils.generate_words(min_count_words=25, max_count_words=30, to_register='capitalize')
        self.assertTrue(words[0].istitle())
        for word in words[1:]:
            self.assertTrue(word.islower())
        # lower
        words = utils.generate_words(min_count_words=25, max_count_words=30, to_register='lower')
        for word in words:
            self.assertTrue(word.islower())
        # upper
        words = utils.generate_words(min_count_words=25, max_count_words=30, to_register='upper')
        for word in words:
            self.assertTrue(word.isupper())
        # title
        words = utils.generate_words(min_count_words=25, max_count_words=30, to_register='title')
        for word in words:
            self.assertTrue(word.istitle())


if __name__ == '__main__':
    unittest.main()
