
from unittest import mock

from django.db.models.fields.files import ImageFieldFile
from django.utils.text import slugify
from django.core.exceptions import ValidationError

import pytest

from apps.replies.factories import ReplyFactory
from apps.tags.models import Tag

from utils.python.logging_utils import create_logger_by_filename
from utils.django.test_utils import EnhancedTestCase
from utils.django.factories_utils import generate_text_by_min_length

from apps.books.factories import BookFactory, WriterFactory
from apps.books.models import Book, Writer

logger = create_logger_by_filename(__name__)


class BookTests(EnhancedTestCase):
    """
    Test for model Book
    """

    @classmethod
    def setUpTestData(cls):

        cls.call_command('factory_test_users', '8')
        cls.call_command('factory_test_writers', '4')

        cls.active_superuser = cls.django_user_model.objects.first()
        cls._make_user_as_active_superuser(cls.active_superuser)

        cls.now_year = cls.timezone.now().year

        cls.book = BookFactory(name='Made boring stuff with Python', pages=49)
        cls.book.replies.clear()

    def setUp(self):

        self.book.refresh_from_db()

    def test_create_book(self):

        data = dict(
            name='Книжка о программировании на Python 3',
            description=generate_text_by_min_length(100, as_p=True),
            picture=self._generate_image(),
            language='ru',
            pages=140,
            publishers='O`Reilly',
            isbn='4515-4579-45478-78129-454',
            year_published=2007,
        )
        book = Book(**data)
        book.full_clean()
        book.save()
        #
        book.tags.add(*Tag.objects.random_tags(3))
        book.authorship.add(*Writer.objects.all()[:3])
        #
        ReplyFactory(content_object=book)
        ReplyFactory(content_object=book)
        ReplyFactory(content_object=book)
        #
        book.refresh_from_db()
        self.assertEqual(book.name, data['name'])
        self.assertEqual(book.slug, slugify(data['name'], allow_unicode=True))
        self.assertEqual(book.description, data['description'])
        self.assertIsInstance(book.picture, ImageFieldFile)
        self.assertEqual(book.language, data['language'])
        self.assertEqual(book.pages, data['pages'])
        self.assertEqual(book.publishers, data['publishers'])
        self.assertEqual(book.isbn, data['isbn'])
        self.assertEqual(book.year_published, data['year_published'])
        self.assertEqual(book.replies.count(), 3)
        self.assertEqual(book.tags.count(), 3)
        self.assertEqual(book.authorship.count(), 3)

    def test_update_book(self):

        data = dict(
            name='Книга рецептов JS с подробными объяснениями и красивым постраничными оформлением.',
            description=generate_text_by_min_length(100, as_p=True),
            picture=self._generate_image(),
            language='ru',
            pages=440,
            publishers='Express',
            isbn='785121-4512-7515-4215-784',
            year_published=2015,
        )
        book = BookFactory()
        book.name = data['name']
        book.description = data['description']
        book.picture = data['picture']
        book.language = data['language']
        book.pages = data['pages']
        book.publishers = data['publishers']
        book.isbn = data['isbn']
        book.year_published = data['year_published']
        book.full_clean()
        book.save()
        self.assertEqual(book.name, data['name'])
        self.assertEqual(book.slug, slugify(data['name'], allow_unicode=True))
        self.assertEqual(book.description, data['description'])
        self.assertIsInstance(book.picture, ImageFieldFile)
        self.assertEqual(book.language, data['language'])
        self.assertEqual(book.pages, data['pages'])
        self.assertEqual(book.publishers, data['publishers'])
        self.assertEqual(book.isbn, data['isbn'])
        self.assertEqual(book.year_published, data['year_published'])

    def test_delete_book(self):

        book = BookFactory()
        book.delete()

    def test_str(self):

        self.assertEqual(str(self.book), 'Made boring stuff with Python')

    def test_unique_slug(self):

        same_name = 'Справочник смелого человека решившегося пойти против течения и найти себя в жизни таким как есть.'
        same_name_as_lower = same_name.lower()
        same_name_as_upper = same_name.upper()
        same_name_as_title = same_name.title()
        slug_same_name = slugify(same_name, allow_unicode=True)
        #
        book1 = BookFactory(name=same_name_as_lower)
        book2 = BookFactory(name=same_name_as_upper)
        book3 = BookFactory(name=same_name_as_title)
        #
        self.assertEqual(book1.name, same_name_as_lower)
        self.assertEqual(book1.slug, slug_same_name)
        self.assertEqual(book2.name, same_name_as_upper)
        self.assertEqual(book2.slug, slug_same_name + '-2')
        self.assertEqual(book3.name, same_name_as_title)
        self.assertEqual(book3.slug, slug_same_name + '-3')

    def test_get_absolute_url(self):

        response = self.client.get(self.book.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_get_admin_url(self):

        book = BookFactory()
        book.replies.clear()

        logger.warning('Book worked only with single ReplyFactory(). Problem in replies.factories.fuzzuinteger')

        ReplyFactory(content_object=book)

        self.client.force_login(self.active_superuser)
        response = self.client.get(book.get_admin_url())
        self.assertEqual(response.status_code, 200)

    def test_upload_book_picture(self):

        path = Book(slug='cassandra-and-apache-on-aws').upload_book_picture('bucket_big_code.png')
        self.assertEqual(path, 'books/cassandra-and-apache-on-aws/bucket_big_code.png')

    def test_get_rating_if_book_has_not_replies(self):

        self.assertEqual(self.book.get_rating(), 0)

    def test_get_rating_if_book_has_replies(self):

        ReplyFactory(content_object=self.book, mark_for_content=3, mark_for_style=1, mark_for_language=2)  # 2
        self.assertEqual(self.book.get_rating(), 2.0)
        ReplyFactory(content_object=self.book, mark_for_content=4, mark_for_style=5, mark_for_language=1)  # 3.3333
        ReplyFactory(content_object=self.book, mark_for_content=5, mark_for_style=4, mark_for_language=5)  # 4.6667
        ReplyFactory(content_object=self.book, mark_for_content=2, mark_for_style=5, mark_for_language=4)  # 3.6667
        self.assertEqual(self.book.get_rating(), 3.4167)

    def test_is_new_if_published_in_this_year(self):

        self.book.year_published = self.now_year
        self.book.full_clean()
        self.book.save()
        self.assertTrue(self.book.is_new())

    def test_is_new_if_published_one_year_ago(self):

        self.book.year_published = self.now_year - 1
        self.book.full_clean()
        self.book.save()
        self.assertTrue(self.book.is_new())

    def test_is_new_if_published_two_years_ago(self):

        self.book.year_published = self.now_year - 2
        self.book.full_clean()
        self.book.save()
        self.assertFalse(self.book.is_new())

    def test_is_new_if_published_three_years_ago(self):

        self.book.year_published = self.now_year - 3
        self.book.full_clean()
        self.book.save()
        self.assertFalse(self.book.is_new())

    def test_get_size_book_with_diffrent_count_pages(self):

        for count_pages, book_size_name in (
            (1, 'Tiny book'),
            (10, 'Tiny book'),
            (49, 'Tiny book'),
            (50, 'Middle book'),
            (100, 'Middle book'),
            (200, 'Middle book'),
            (299, 'Middle book'),
            (300, 'Big book'),
            (400, 'Big book'),
            (500, 'Big book'),
            (599, 'Big book'),
            (600, 'Big book'),
            (700, 'Big book'),
            (800, 'Big book'),
            (900, 'Big book'),
            (999, 'Big book'),
            (1000, 'Great book'),
            (2000, 'Great book'),
        ):
            self.book.pages = count_pages
            self.book.full_clean()
            self.book.save()
            self.assertEqual(self.book.get_size(), book_size_name)

    def test_most_common_words_from_replies_if_book_has_not_replies(self):

        self.assertEqual(self.book.most_common_words_from_replies(), [])

    def test_most_common_words_from_replies_if_book_has_replies(self):
        ReplyFactory(
            content_object=self.book,
            advantages=['Perfect', 'Good', 'Nice', 'Interesting', 'Amazing', 'Fantastic', 'Alluring'],
            disadvantages=['Small', 'Strange']
        )
        ReplyFactory(
            content_object=self.book,
            advantages=['Nice', 'Strange', 'Amazing', 'Fantastic'],
            disadvantages=['Bad', 'Obvious', 'Fuzzy', 'Non-interesting']
        )
        ReplyFactory(
            content_object=self.book,
            advantages=['Perfect', 'Good', 'Nice', 'Strange', 'Amazing', 'Dizzy'],
            disadvantages=['Small', 'Blurred']
        )
        ReplyFactory(
            content_object=self.book,
            advantages=['Perfect', 'Good', 'Nice', 'Strange', 'Amazing', 'Fantastic'],
            disadvantages=['Small', 'Bad', 'Fuzzy', 'Strange', 'Non-interesting']
        )

        most_common_words_from_replies = self.book.most_common_words_from_replies()
        self.assertCountEqual(most_common_words_from_replies, [
            ('Fantastic', 3), ('Perfect', 3), ('Good', 3), ('Amazing', 4), ('Nice', 4),
            ('Small', 3), ('Strange', 5), ('Fuzzy', 2), ('Bad', 2), ('Non-interesting', 2)
        ])
        self.assertCountEqual(
            most_common_words_from_replies[-3:],
            [('Fuzzy', 2), ('Bad', 2), ('Non-interesting', 2)]
        )
        self.assertCountEqual(
            most_common_words_from_replies[1:3], [('Amazing', 4), ('Nice', 4)]
        )
        self.assertCountEqual(
            most_common_words_from_replies[3:-3],
            [('Fantastic', 3), ('Perfect', 3), ('Good', 3), ('Small', 3)]
        )
        self.assertEqual(most_common_words_from_replies[0], ('Strange', 5))


class WriterTests(EnhancedTestCase):
    """
    Tests for the model Writer
    """

    @classmethod
    def setUpTestData(cls):

        cls.call_command('factory_test_users', '8')
        cls.call_command('factory_test_writers', '4')

        cls.active_superuser = cls.django_user_model.objects.first()
        cls._make_user_as_active_superuser(cls.active_superuser)

        cls.writer = Writer.objects.first()

        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = cls.timezone.datetime(2016, 11, 11)
            cls.now_year = cls.timezone.now().year

        cls.writer = WriterFactory()

    def setUp(self):

        self.writer.refresh_from_db()

    def test_create_writer(self):

        data = dict(
            name='Nanvel Olexander',
            about=generate_text_by_min_length(100, as_p=True),
            years_life='1990 - ',
        )
        writer = Writer(**data)
        writer.full_clean()
        writer.save()
        self.assertEqual(writer.name, data['name'])
        self.assertEqual(writer.slug, slugify(data['name'], allow_unicode=True))
        self.assertEqual(writer.about, data['about'])
        self.assertEqual(writer.years_life, data['years_life'])

    def test_update_writer(self):

        data = dict(
            name='Daniel Roseman',
            about=generate_text_by_min_length(100, as_p=True),
            years_life='1980 - ',
        )
        self.writer.name = data['name']
        self.writer.about = data['about']
        self.writer.years_life = data['years_life']
        self.writer.full_clean()
        self.writer.save()
        self.assertEqual(self.writer.name, data['name'])
        self.assertEqual(self.writer.slug, slugify(data['name'], allow_unicode=True))
        self.assertEqual(self.writer.about, data['about'])
        self.assertEqual(self.writer.years_life, data['years_life'])

    def test_delete_writer(self):

        writer = WriterFactory()
        writer.delete()

    def test_unique_slug(self):

        same_name = 'русский Омар Хайам ибн Рахман Дулиб али Алькуманди Парандреус Кавказинидзе Агипян Младший'
        same_name_as_lower = same_name.lower()
        same_name_as_upper = same_name.upper()
        same_name_as_title = same_name.title()
        slug_same_name = slugify(same_name, allow_unicode=True)
        #
        writer1 = WriterFactory()
        writer2 = WriterFactory()
        writer3 = WriterFactory()
        #
        writer1.name = same_name_as_lower
        writer2.name = same_name_as_upper
        writer3.name = same_name_as_title
        #
        writer1.full_clean()
        writer2.full_clean()
        writer3.full_clean()
        #
        writer1.save()
        writer2.save()
        writer3.save()
        #
        self.assertEqual(writer1.name, same_name_as_lower)
        self.assertEqual(writer1.slug, slug_same_name)
        self.assertEqual(writer2.name, same_name_as_upper)
        self.assertEqual(writer2.slug, slug_same_name + '-2')
        self.assertEqual(writer3.name, same_name_as_title)
        self.assertEqual(writer3.slug, slug_same_name + '-3')

    def test_get_absolute_url(self):

        self.client.force_login(self.active_superuser)
        response = self.client.get(self.writer.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_get_admin_url(self):

        self.client.force_login(self.active_superuser)
        response = self.client.get(self.writer.get_admin_url())
        self.assertEqual(response.status_code, 200)

    def test_year_birth_is_range_from_1900_to_2000_or_sign_question(self):

        self.writer.years_life = '? - '
        self.writer.full_clean()

        for year in range(1900, 2000 + 1):
            self.writer.years_life = '{} - '.format(year)
            self.writer.full_clean()

    def test_year_birth_is_out_of_range_acceptable_years(self):

        with self.assertRaisesMessage(ValidationError, 'Invalid years life of a writer.'):
            self.writer.years_life = '1899 - '
            self.writer.full_clean()

        with self.assertRaisesMessage(ValidationError, 'Invalid years life of a writer.'):
            self.writer.years_life = '2001 - '
            self.writer.full_clean()

    def test_year_birth_is_none_year_death_is_early_1915(self):

        with self.assertRaisesMessage(ValidationError, 'Invalid years life of a writer.'):
            self.writer.years_life = '? - 1914'
            self.writer.full_clean()

    def test_year_death_not_possible_in_future(self):

        with self.assertRaisesMessage(ValidationError, 'Year death of a writer not possible in future.'):
            self.writer.years_life = '? - {0}'.format(self.now_year + 1)
            self.writer.full_clean()

        with self.assertRaisesMessage(ValidationError, 'Year death of a writer not possible in future.'):
            self.writer.years_life = '1990 - {0}'.format(self.now_year + 1)
            self.writer.full_clean()

    def test_if_birth_year_is_more_or_equal_year_dead(self):

        with self.assertRaisesMessage(ValidationError, 'Year of birth can not more or equal year of death.'):
            self.writer.years_life = '1999 - 1998'
            self.writer.full_clean()

        with self.assertRaisesMessage(ValidationError, 'Year of birth can not more or equal year of death.'):
            self.writer.years_life = '1999 - 1999'
            self.writer.full_clean()

    def test_if_small_range_beetween_death_year_and_year_birth(self):

        for year in range(1991, 2005):
            with self.assertRaisesMessage(
                ValidationError,
                'Very small range years between year of birth and year of death of a writer.'
            ):
                self.writer.years_life = '1990 - {0}'.format(year)
                self.writer.full_clean()

        for year in range(2005, 2016):
            self.writer.years_life = '1990 - {0}'.format(year)
            self.writer.full_clean()

    def test_get_age_of_writer(self):

        self.writer.years_life = '? - ?'
        self.writer.full_clean()
        self.writer.save()
        self.assertIsNone(self.writer.get_age(), )

        self.writer.years_life = '? - 2016'
        self.writer.full_clean()
        self.writer.save()
        self.assertIsNone(self.writer.get_age(), )

        self.writer.years_life = '? - '
        self.writer.full_clean()
        self.writer.save()
        self.assertIsNone(self.writer.get_age(), )

        self.writer.years_life = '1990 - ?'
        self.writer.full_clean()
        self.writer.save()
        self.assertIsNone(self.writer.get_age(), )

        self.writer.years_life = '2000 - '
        self.writer.full_clean()
        self.writer.save()
        self.assertEqual(self.writer.get_age(), 16)

        self.writer.years_life = '1950 - 2013'
        self.writer.full_clean()
        self.writer.save()
        self.assertEqual(self.writer.get_age(), 63)

    def test_get_avg_mark_for_books_if_writer_has_no_books(self):

        self.writer.books.clear()
        self.assertEqual(self.writer.get_avg_mark_for_books(), 0.0)

    def test_get_avg_mark_for_books_if_writer_has_books(self):

        # rating first book 4.0
        book1 = BookFactory()
        book1.authorship.set([self.writer])
        book1.replies.clear()
        ReplyFactory(content_object=book1, mark_for_content=3, mark_for_style=5, mark_for_language=4)  # 4
        self.assertEqual(self.writer.get_avg_mark_for_books(), 4.0)

        # rating second book 3
        book2 = BookFactory()
        book2.authorship.set([self.writer])
        book2.replies.clear()
        ReplyFactory(content_object=book2, mark_for_content=3, mark_for_style=1, mark_for_language=5)  # 3
        ReplyFactory(content_object=book2, mark_for_content=1, mark_for_style=1, mark_for_language=1)  # 1
        ReplyFactory(content_object=book2, mark_for_content=5, mark_for_style=5, mark_for_language=5)  # 5

        # rating first book 4.0, second - 3.0 = (4 + 3) / 2
        self.assertEqual(self.writer.get_avg_mark_for_books(), 3.5)

        # rating third book 3.6667
        book3 = BookFactory()
        book3.authorship.set([self.writer])
        book3.replies.clear()
        ReplyFactory(content_object=book3, mark_for_content=4, mark_for_style=5, mark_for_language=5)  # 4.6667
        ReplyFactory(content_object=book3, mark_for_content=1, mark_for_style=5, mark_for_language=2)  # 2.6667

        # rating first book 4.0, second - 3.0, third - 3.6667 = (4 + 3+ 3.6667) / 3
        self.assertEqual(self.writer.get_avg_mark_for_books(), 3.556)
