
import random

from django.utils.text import slugify
from django.core.exceptions import ValidationError

import pytest

from apps.replies.factories import ReplyFactory
from apps.tags.models import Tag

from mylabour.test_utils import EnhancedTestCase
from mylabour.factories_utils import generate_text_by_min_length

from apps.books.factories import BookFactory, WriterFactory
from apps.books.models import Book, Writer


class BookTest(EnhancedTestCase):
    """
    Test for model Book
    """

    @classmethod
    def setUpTestData(cls):
        cls.call_command('factory_test_users', '15')
        cls.call_command('factory_test_writers', '15')

        cls.active_superuser = cls.django_user_model.objects.first()
        cls._make_user_as_active_superuser(cls.active_superuser)

        cls.now_year = cls.timezone.now().year

    def setUp(self):
        self.book = BookFactory()

    def test_create_book(self):
        data = dict(
            name='Книжка о программировании на Python 3',
            description=generate_text_by_min_length(100, as_p=True),
            picture='http://transcad.com/miranda.jpeg',
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
        self.assertEqual(book.picture, data['picture'])
        self.assertEqual(book.language, data['language'])
        self.assertEqual(book.pages, data['pages'])
        self.assertEqual(book.publishers, data['publishers'])
        self.assertEqual(book.isbn, data['isbn'])
        self.assertEqual(book.year_published, data['year_published'])
        self.assertEqual(book.replies.count(), 3)
        self.assertEqual(book.tags.count(), 3)
        self.assertEqual(book.authorship.count(), 3)

    def test_update_book(self):
        # choice random language
        languages_without_already_used = filter(lambda couple: couple[0] != self.book.language, Book.LANGUAGES)
        another_language = random.choice(tuple(languages_without_already_used))[0]
        #
        data = dict(
            name='Книга рецептов JS с подробными объяснениями и красивым постраничными оформлением.',
            description=generate_text_by_min_length(100, as_p=True),
            picture='http://using.com/anaconda.png',
            language=another_language,
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
        self.assertEqual(book.picture, data['picture'])
        self.assertEqual(book.language, data['language'])
        self.assertEqual(book.pages, data['pages'])
        self.assertEqual(book.publishers, data['publishers'])
        self.assertEqual(book.isbn, data['isbn'])
        self.assertEqual(book.year_published, data['year_published'])

    def test_delete_book(self):
        self.book.delete()

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
        self.client.force_login(self.active_superuser)
        response = self.client.get(self.book.get_admin_url())
        self.assertEqual(response.status_code, 200)

    def test_get_rating(self):
        self.book.replies.clear()
        self.assertEqual(self.book.get_rating(), 0)
        ReplyFactory(content_object=self.book, scope_for_content=3, scope_for_style=1, scope_for_language=2)  # 2
        self.assertEqual(self.book.get_rating(), 2.0)
        ReplyFactory(content_object=self.book, scope_for_content=4, scope_for_style=5, scope_for_language=1)  # 3.3333
        ReplyFactory(content_object=self.book, scope_for_content=5, scope_for_style=4, scope_for_language=5)  # 4.6667
        ReplyFactory(content_object=self.book, scope_for_content=2, scope_for_style=5, scope_for_language=4)  # 3.6667
        self.assertEqual(self.book.get_rating(), 3.4167)

    def test_is_new(self):
        #
        self.book.year_published = self.now_year
        self.book.full_clean()
        self.book.save()
        #
        new_book1 = BookFactory()
        new_book2 = BookFactory()
        new_book3 = BookFactory()
        new_book1.year_published = self.now_year - 1
        new_book2.year_published = self.now_year - 2
        new_book3.year_published = self.now_year - 3
        new_book1.full_clean()
        new_book2.full_clean()
        new_book3.full_clean()
        new_book1.save()
        new_book2.save()
        new_book3.save()
        #
        self.assertTrue(self.book.is_new())
        self.assertTrue(new_book1.is_new())
        self.assertFalse(new_book2.is_new())
        self.assertFalse(new_book3.is_new())

    def test_get_size(self):
        self.book.pages = 40
        self.book.full_clean()
        self.book.save()
        self.assertEqual(self.book.get_size(), 'Tiny book')

    def test_most_common_words_from_replies(self):
        self.book.replies.clear()
        self.assertEqual(self.book.most_common_words_from_replies(), [])
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


class WriterTest(EnhancedTestCase):
    """
    Test for model Writer
    """

    @classmethod
    def setUpTestData(cls):
        cls.call_command('factory_test_users', '15')
        cls.call_command('factory_test_writers', '15')

        cls.active_superuser = cls.django_user_model.objects.first()
        cls._make_user_as_active_superuser(cls.active_superuser)

        cls.writer = Writer.objects.first()

        cls.now_year = cls.timezone.now().year

    def setUp(self):
        self.writer = WriterFactory()

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
        self.writer.delete()

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
        response = self.client.get(self.writer.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_year_death_not_possible_in_future(self):

        self.writer.years_life = '? - {0}'.format(self.now_year + 1)
        self.assertRaisesMessage(ValidationError, 'Year death of writer not possible in future.', self.writer.full_clean)

    @pytest.mark.xfail(run=False)
    def test_if_birth_year_is_more_or_equal_year_dead(self):
        self.writer.years_life = NumericRange(1990, 1950)
        self.assertRaisesMessage(
            ValidationError, 'Year of birth can not more or equal year of dearth.', self.writer.full_clean
        )
        self.writer.years_life = NumericRange(1988, 1988)
        self.assertRaisesMessage(
            ValidationError, 'Year of birth can not more or equal year of dearth.', self.writer.full_clean
        )

    @pytest.mark.xfail(run=False)
    def test_if_small_range_beetween_death_year_and_year_birth(self):
        self.writer.years_life = NumericRange(1990, 1991)
        self.assertRaisesMessage(
            ValidationError, 'Very small range between year of birth and year of death.', self.writer.full_clean
        )
        self.writer.years_life = NumericRange(1990, 2009)
        self.assertRaisesMessage(
            ValidationError, 'Very small range between year of birth and year of death.', self.writer.full_clean
        )
        # difference must be 20 and more
        self.writer.years_life = NumericRange(1960, 1980)
        self.writer.full_clean()
        self.writer.years_life = NumericRange(1960, 1981)
        self.writer.full_clean()

    @pytest.mark.xfail(run=False)
    def test_if_big_range_beetween_death_year_and_year_birth(self):
        self.writer.years_life = NumericRange(1800, 2000)
        self.assertRaisesMessage(
            ValidationError, 'Very big range between year of birth and year of death (200 years).', self.writer.full_clean
        )
        self.writer.years_life = NumericRange(1800, 1901)
        self.assertRaisesMessage(
            ValidationError, 'Very big range between year of birth and year of death (101 years).', self.writer.full_clean
        )
        # diffence must be less or equal 100
        self.writer.years_life = NumericRange(1800, 1900)
        self.writer.full_clean()
        self.writer.years_life = NumericRange(1800, 1899)
        self.writer.full_clean()

    @pytest.mark.xfail(run=False)
    def test_if_very_young_writer(self):
        self.writer.years_life = NumericRange(self.now_year - 1, None)
        self.assertRaisesMessage(
            ValidationError, 'Writer may can bithed only from 1000 A. D. to 1996 year.', self.writer.full_clean
        )
        self.writer.years_life = NumericRange(self.now_year - 19, None)
        self.assertRaisesMessage(
            ValidationError, 'Writer may can bithed only from 1000 A. D. to 1996 year.', self.writer.full_clean
        )
        # wrriter may can born only 20 years ago or more
        self.writer.years_life = NumericRange(self.now_year - 20, None)
        self.writer.full_clean()

    @pytest.mark.xfail(run=False)
    def test_get_age_of_writer(self):
        writer1 = WriterFactory(years_life=NumericRange(1950, 2013))
        writer2 = WriterFactory(years_life=NumericRange(1990, None))
        writer3 = WriterFactory(years_life=NumericRange(None, None))
        writer4 = WriterFactory(years_life=NumericRange(None, 2016))
        #
        self.assertEqual(writer1.get_age(), 63)
        self.assertIsNone(writer2.get_age())
        self.assertIsNone(writer3.get_age())
        self.assertIsNone(writer4.get_age())

    @pytest.mark.xfail(run=False)
    def test_show_years_life(self):
        writer1 = WriterFactory(years_life=NumericRange(1877, 1928))
        writer2 = WriterFactory(years_life=NumericRange(1990, None))
        writer3 = WriterFactory(years_life=NumericRange(None, None))
        writer4 = WriterFactory(years_life=NumericRange(None, 2016))
        #
        self.assertEqual(writer1.show_years_life(), '1877 - 1928')
        self.assertEqual(writer2.show_years_life(), '1990 - ????')
        self.assertEqual(writer3.show_years_life(), '???? - ????')
        self.assertEqual(writer4.show_years_life(), '???? - 2016')

    def test_get_avg_scope_for_books(self):
        # without books
        self.writer.books.clear()
        self.assertEqual(self.writer.get_avg_scope_for_books(), 0)
        # books
        # rating first book 4.0
        book1 = BookFactory()
        book1.authorship.set([self.writer])
        book1.replies.clear()
        ReplyFactory(content_object=book1, scope_for_content=3, scope_for_style=5, scope_for_language=4)  # 4
        self.assertEqual(self.writer.get_avg_scope_for_books(), 4.0)
        # rating second book 3
        book2 = BookFactory()
        book2.authorship.set([self.writer])
        book2.replies.clear()
        ReplyFactory(content_object=book2, scope_for_content=3, scope_for_style=1, scope_for_language=5)  # 3
        ReplyFactory(content_object=book2, scope_for_content=1, scope_for_style=1, scope_for_language=1)  # 1
        ReplyFactory(content_object=book2, scope_for_content=5, scope_for_style=5, scope_for_language=5)  # 5
        self.assertEqual(self.writer.get_avg_scope_for_books(), 3.5)
        # rating third book 3.6667
        book3 = BookFactory()
        book3.authorship.set([self.writer])
        book3.replies.clear()
        ReplyFactory(content_object=book3, scope_for_content=4, scope_for_style=5, scope_for_language=5)  # 4.6667
        ReplyFactory(content_object=book3, scope_for_content=1, scope_for_style=5, scope_for_language=2)  # 2.6667
        self.assertEqual(self.writer.get_avg_scope_for_books(), 3.5557)
