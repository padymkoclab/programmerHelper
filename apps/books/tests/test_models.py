
import random

from django.utils import timezone
from django.utils.text import slugify
from django.test import TestCase
from django.core.exceptions import ValidationError

from psycopg2.extras import NumericRange

from apps.accounts.factories import accounts_factory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory
from apps.replies.factories import ReplyFactory
from apps.tags.models import Tag
from apps.web_links.models import WebLink
from mylabour.utils import generate_text_by_min_length

from apps.books.factories import BookFactory, WritterFactory, books_factory, writters_factory
from apps.books.models import Book, Writter


NOW_YEAR = timezone.datetime.now().year


class BookTest(TestCase):
    """
    Test for model Book
    """

    @classmethod
    def setUpTestData(cls):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)
        writters_factory(15)

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
        book.links.add(*WebLink.objects.random_weblinks(4))
        book.accounts.add(*Writter.objects.all()[:3])
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
        self.assertEqual(book.links.count(), 4)
        self.assertEqual(book.accounts.count(), 3)

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
        same_name = 'Справочник смелого программиста решившегося пойти против течения и найти себя в жизни таким как есть.'
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
        self.book.year_published = NOW_YEAR
        self.book.full_clean()
        self.book.save()
        #
        new_book1 = BookFactory()
        new_book2 = BookFactory()
        new_book3 = BookFactory()
        new_book1.year_published = NOW_YEAR - 1
        new_book2.year_published = NOW_YEAR - 2
        new_book3.year_published = NOW_YEAR - 3
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
        self.assertCountEqual(most_common_words_from_replies[-3:], [('Fuzzy', 2), ('Bad', 2), ('Non-interesting', 2)])
        self.assertCountEqual(most_common_words_from_replies[1:3], [('Amazing', 4), ('Nice', 4)])
        self.assertCountEqual(most_common_words_from_replies[3:-3], [('Fantastic', 3), ('Perfect', 3), ('Good', 3), ('Small', 3)])
        self.assertEqual(most_common_words_from_replies[0], ('Strange', 5))


class WritterTest(TestCase):
    """
    Test for model Writter
    """

    @classmethod
    def setUpTestData(cls):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)
        books_factory(10)

    def setUp(self):
        self.writter = WritterFactory()

    def test_create_writter(self):
        data = dict(
            name='Николай Левашов',
            about=generate_text_by_min_length(100, as_p=True),
            years_life=NumericRange(1960, 2012),
        )
        writter = Writter(**data)
        writter.full_clean()
        writter.save()
        self.assertEqual(writter.name, data['name'])
        self.assertEqual(writter.slug, slugify(data['name'], allow_unicode=True))
        self.assertEqual(writter.about, data['about'])
        self.assertEqual(writter.years_life, data['years_life'])

    def test_update_writter(self):
        data = dict(
            name='Валерий Дёмин',
            about=generate_text_by_min_length(100, as_p=True),
            years_life=NumericRange(1950, 2016),
        )
        self.writter.name = data['name']
        self.writter.about = data['about']
        self.writter.years_life = data['years_life']
        self.writter.full_clean()
        self.writter.save()
        self.assertEqual(self.writter.name, data['name'])
        self.assertEqual(self.writter.slug, slugify(data['name'], allow_unicode=True))
        self.assertEqual(self.writter.about, data['about'])
        self.assertEqual(self.writter.years_life, data['years_life'])

    def test_delete_writter(self):
        self.writter.delete()

    def test_unique_slug(self):
        same_name = 'русский Омар Хайам ибн Рахман Дулиб али Алькуманди Парандреус Кавказинидзе Агипян Младший'
        same_name_as_lower = same_name.lower()
        same_name_as_upper = same_name.upper()
        same_name_as_title = same_name.title()
        slug_same_name = slugify(same_name, allow_unicode=True)
        #
        writter1 = WritterFactory()
        writter2 = WritterFactory()
        writter3 = WritterFactory()
        #
        writter1.name = same_name_as_lower
        writter2.name = same_name_as_upper
        writter3.name = same_name_as_title
        #
        writter1.full_clean()
        writter2.full_clean()
        writter3.full_clean()
        #
        writter1.save()
        writter2.save()
        writter3.save()
        #
        self.assertEqual(writter1.name, same_name_as_lower)
        self.assertEqual(writter1.slug, slug_same_name)
        self.assertEqual(writter2.name, same_name_as_upper)
        self.assertEqual(writter2.slug, slug_same_name + '-2')
        self.assertEqual(writter3.name, same_name_as_title)
        self.assertEqual(writter3.slug, slug_same_name + '-3')

    def test_get_absolute_url(self):
        response = self.client.get(self.writter.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_accept_only_None_or_integer_as_values_for_field_years_life(self):
        # non accepted values
        self.writter.years_life = NumericRange('text', 1.1)
        self.assertRaisesMessage(ValidationError, 'Year birth and death must be integer or skiped.', self.writter.full_clean)
        self.writter.years_life = NumericRange(None, 'string')
        self.assertRaisesMessage(ValidationError, 'Year birth and death must be integer or skiped.', self.writter.full_clean)
        self.writter.years_life = NumericRange('string', None)
        self.assertRaisesMessage(ValidationError, 'Year birth and death must be integer or skiped.', self.writter.full_clean)
        self.writter.years_life = NumericRange('string', 1111)
        self.assertRaisesMessage(ValidationError, 'Year birth and death must be integer or skiped.', self.writter.full_clean)
        self.writter.years_life = NumericRange(1111, 1.1)
        self.assertRaisesMessage(ValidationError, 'Year birth and death must be integer or skiped.', self.writter.full_clean)
        self.writter.years_life = NumericRange(True, None)
        self.assertRaisesMessage(ValidationError, 'Year birth and death must be integer or skiped.', self.writter.full_clean)
        self.writter.years_life = NumericRange(None, False)
        self.assertRaisesMessage(ValidationError, 'Year birth and death must be integer or skiped.', self.writter.full_clean)
        # accepted values
        self.writter.years_life = NumericRange(None, None)
        self.writter.full_clean()
        self.writter.years_life = NumericRange(None, 1000)
        self.writter.full_clean()
        self.writter.years_life = NumericRange(1000, None)
        self.writter.full_clean()
        self.writter.years_life = NumericRange(1000, 1050)

    def test_restrict_year_birth(self):
        # look over range years from -100 A.D. to now + 1 year
        for year_birth in range(-100, NOW_YEAR + 2):
            self.writter.years_life = NumericRange(year_birth, None)
            # look over birth year from 1000 to 20 years ago
            if year_birth in range(1000, NOW_YEAR - 19):
                self.writter.full_clean()
            else:
                self.assertRaisesMessage(
                    ValidationError, 'Writter may can bithed only from 1000 A. D. to {0} year.'.format(NOW_YEAR - 20),
                    self.writter.full_clean
                )

    def test_restrict_year_death(self):
        # look over range years from -100 A.D. to now + 1 year
        for year_death in range(-100, NOW_YEAR + 2):
            self.writter.years_life = NumericRange(None, year_death)
            if year_death in range(1000, NOW_YEAR + 1):
                self.writter.full_clean()
            else:
                self.assertRaisesMessage(
                    ValidationError, 'Writter may can dead only from 1000 A. D. to now year.',
                    self.writter.full_clean
                )

    def test_if_birth_year_is_more_or_equal_year_dead(self):
        self.writter.years_life = NumericRange(1990, 1950)
        self.assertRaisesMessage(
            ValidationError, 'Year of birth can not more or equal year of dearth.', self.writter.full_clean
        )
        self.writter.years_life = NumericRange(1988, 1988)
        self.assertRaisesMessage(
            ValidationError, 'Year of birth can not more or equal year of dearth.', self.writter.full_clean
        )

    def test_if_small_range_beetween_death_year_and_year_birth(self):
        self.writter.years_life = NumericRange(1990, 1991)
        self.assertRaisesMessage(
            ValidationError, 'Very small range between year of birth and year of death.', self.writter.full_clean
        )
        self.writter.years_life = NumericRange(1990, 2009)
        self.assertRaisesMessage(
            ValidationError, 'Very small range between year of birth and year of death.', self.writter.full_clean
        )
        # difference must be 20 and more
        self.writter.years_life = NumericRange(1960, 1980)
        self.writter.full_clean()
        self.writter.years_life = NumericRange(1960, 1981)
        self.writter.full_clean()

    def test_if_big_range_beetween_death_year_and_year_birth(self):
        self.writter.years_life = NumericRange(1800, 2000)
        self.assertRaisesMessage(
            ValidationError, 'Very big range between year of birth and year of death (200 years).', self.writter.full_clean
        )
        self.writter.years_life = NumericRange(1800, 1901)
        self.assertRaisesMessage(
            ValidationError, 'Very big range between year of birth and year of death (101 years).', self.writter.full_clean
        )
        # diffence must be less or equal 100
        self.writter.years_life = NumericRange(1800, 1900)
        self.writter.full_clean()
        self.writter.years_life = NumericRange(1800, 1899)
        self.writter.full_clean()

    def test_if_very_young_writter(self):
        self.writter.years_life = NumericRange(NOW_YEAR - 1, None)
        self.assertRaisesMessage(
            ValidationError, 'Writter may can bithed only from 1000 A. D. to 1996 year.', self.writter.full_clean
        )
        self.writter.years_life = NumericRange(NOW_YEAR - 19, None)
        self.assertRaisesMessage(
            ValidationError, 'Writter may can bithed only from 1000 A. D. to 1996 year.', self.writter.full_clean
        )
        # wrriter may can born only 20 years ago or more
        self.writter.years_life = NumericRange(NOW_YEAR - 20, None)
        self.writter.full_clean()

    def test_get_age_of_writter(self):
        writter1 = WritterFactory(years_life=NumericRange(1950, 2013))
        writter2 = WritterFactory(years_life=NumericRange(1990, None))
        writter3 = WritterFactory(years_life=NumericRange(None, None))
        writter4 = WritterFactory(years_life=NumericRange(None, 2016))
        #
        self.assertEqual(writter1.get_age(), 63)
        self.assertIsNone(writter2.get_age())
        self.assertIsNone(writter3.get_age())
        self.assertIsNone(writter4.get_age())

    def test_show_years_life(self):
        writter1 = WritterFactory(years_life=NumericRange(1877, 1928))
        writter2 = WritterFactory(years_life=NumericRange(1990, None))
        writter3 = WritterFactory(years_life=NumericRange(None, None))
        writter4 = WritterFactory(years_life=NumericRange(None, 2016))
        #
        self.assertEqual(writter1.show_years_life(), '1877 - 1928')
        self.assertEqual(writter2.show_years_life(), '1990 - ????')
        self.assertEqual(writter3.show_years_life(), '???? - ????')
        self.assertEqual(writter4.show_years_life(), '???? - 2016')

    def test_get_avg_scope_for_books(self):
        # without books
        self.writter.books.clear()
        self.assertEqual(self.writter.get_avg_scope_for_books(), 0)
        # books
        # rating first book 4.0
        book1 = BookFactory()
        book1.accounts.set([self.writter])
        book1.replies.clear()
        ReplyFactory(content_object=book1, scope_for_content=3, scope_for_style=5, scope_for_language=4)  # 4
        self.assertEqual(self.writter.get_avg_scope_for_books(), 4.0)
        # rating second book 3
        book2 = BookFactory()
        book2.accounts.set([self.writter])
        book2.replies.clear()
        ReplyFactory(content_object=book2, scope_for_content=3, scope_for_style=1, scope_for_language=5)  # 3
        ReplyFactory(content_object=book2, scope_for_content=1, scope_for_style=1, scope_for_language=1)  # 1
        ReplyFactory(content_object=book2, scope_for_content=5, scope_for_style=5, scope_for_language=5)  # 5
        self.assertEqual(self.writter.get_avg_scope_for_books(), 3.5)
        # rating third book 3.6667
        book3 = BookFactory()
        book3.accounts.set([self.writter])
        book3.replies.clear()
        ReplyFactory(content_object=book3, scope_for_content=4, scope_for_style=5, scope_for_language=5)  # 4.6667
        ReplyFactory(content_object=book3, scope_for_content=1, scope_for_style=5, scope_for_language=2)  # 2.6667
        self.assertEqual(self.writter.get_avg_scope_for_books(), 3.5556)
