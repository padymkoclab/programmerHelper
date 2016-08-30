
from django.db.models.fields.files import ImageFieldFile

from mylabour.test_utils import EnhancedTestCase

from apps.comments.factories import CommentFactory
from apps.opinions.factories import OpinionFactory
from apps.utilities.models import UtilityCategory, Utility
from apps.utilities.factories import UtilityFactory, UtilityCategoryFactory


class UtilityCategoryTests(EnhancedTestCase):

    @classmethod
    def setUpTestData(cls):

        cls.call_command('factory_test_users', '10')

        cls.active_superuser, cls.user2, cls.user3, cls.user4, cls.user5 =\
            cls.django_user_model._default_manager.all()[:5]

        cls._make_user_as_active_superuser(cls.active_superuser)

        cls.category = UtilityCategoryFactory(name='Chrome extensions')
        cls.category.utilities.filter().delete()

    def setUp(self):

        self.category.refresh_from_db()

    def test_create_utility(self):

        data = {
            'name': 'Sublime Text 3 Plugins',
            'description': """
                Distributed testing with dist mode set to load will report
                on the combined coverage of all slaves.
                The slaves may be spread out over any number of hosts and
                each slave may be located anywhere on the file system.
                Each slave will have its subprocesses measured.
            """,
            'image': self._generate_image()
        }

        category = UtilityCategory(**data)
        category.full_clean()
        category.save()

        self.assertEqual(category.name, data['name'])
        self.assertEqual(category.slug, 'sublime-text-3-plugins')
        self.assertEqual(category.description, data['description'])
        self.assertIsInstance(category.image, ImageFieldFile)

    def test_update_utility(self):

        data = {
            'name': 'Django reusable applications',
            'description': """
                This plugin produces coverage reports.
                It supports centralised testing and distributed testing
                in both load and each modes. It also supports coverage of subprocesses.
                All features offered by the coverage package should be available,
                either through pytest-cov or through coverage’s config file.
            """,
            'image': self._generate_image(),
        }

        self.assertNotEqual(self.category.name, data['name'])
        self.assertNotEqual(self.category.description, data['description'])

        self.category.name = data['name']
        self.category.description = data['description']
        self.category.image = data['image']

        self.category.full_clean()
        self.category.save()

        self.assertEqual(self.category.name, data['name'])
        self.assertEqual(self.category.slug, 'django-reusable-applications')
        self.assertEqual(self.category.description, data['description'])
        self.assertIsInstance(self.category.image, ImageFieldFile)

    def test_delete_category(self):

        category = UtilityCategoryFactory()
        category.delete()

        with self.assertRaises(category.DoesNotExist):
            category.refresh_from_db()

    def test_str(self):
        self.assertEqual(str(self.category), 'Chrome extensions')

    def test_get_absolute_url(self):

        response = self.client.get(self.category.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_get_admin_url(self):

        self.client.force_login(self.active_superuser)
        response = self.client.get(self.category.get_admin_url())
        self.assertEqual(response.status_code, 200)

    def test_get_count_utilities_if_has_attribute_count_utilities(self):

        self.category.count_utilities = 78458754
        self.assertEqual(self.category.get_count_utilities(), 78458754)
        del self.category.count_utilities

    def test_get_count_utilities_if_has_no_utilities(self):

        self.assertEqual(self.category.get_count_utilities(), 0)

    def test_get_count_utilities_if_has_one_utility(self):

        UtilityFactory(category=self.category)
        self.assertEqual(self.category.get_count_utilities(), 1)

    def test_get_count_utilities_if_has_several_utilities(self):

        UtilityFactory(category=self.category)
        UtilityFactory(category=self.category)
        UtilityFactory(category=self.category)
        self.assertEqual(self.category.get_count_utilities(), 3)

    def test_get_total_count_comments_if_no_utilities(self):

        self.assertEqual(self.category.get_total_count_comments(), 0)

    def test_get_total_count_comments_if_has_attribute_total_count_comments(self):

        self.category.total_count_comments = -75454242
        self.assertEqual(self.category.get_total_count_comments(), -75454242)
        del self.category.total_count_comments

    def test_get_total_count_comments_if_has_utilities_without_comments(self):

        utility = UtilityFactory(category=self.category)
        utility.comments.clear()
        utility = UtilityFactory(category=self.category)
        utility.comments.clear()

        self.assertEqual(self.category.get_total_count_comments(), 0)

    def test_get_total_count_comments_if_has_utilities_with_comments(self):

        utility = UtilityFactory(category=self.category)
        utility.comments.clear()

        utility = UtilityFactory(category=self.category)
        utility.comments.clear()
        CommentFactory(content_object=utility)

        utility = UtilityFactory(category=self.category)
        utility.comments.clear()
        CommentFactory(content_object=utility)
        CommentFactory(content_object=utility)

        utility = UtilityFactory(category=self.category)
        utility.comments.clear()
        CommentFactory(content_object=utility)
        CommentFactory(content_object=utility)
        CommentFactory(content_object=utility)

        self.assertEqual(self.category.get_total_count_comments(), 6)

    def test_get_total_count_opinions_if_has_attribute_total_count_opinions(self):

        self.category.total_count_opinions = 1525454
        self.assertEqual(self.category.get_total_count_opinions(), 1525454)
        del self.category.total_count_opinions

    def test_get_total_count_opinions_if_no_utilities(self):

        self.assertEqual(self.category.get_total_count_opinions(), 0)

    def test_get_total_count_opinions_if_has_utilities_without_opinions(self):

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()
        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()

        self.assertEqual(self.category.get_total_count_opinions(), 0)

    def test_get_total_count_opinions_if_has_utilities_with_opinions(self):

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()
        OpinionFactory(content_object=utility)

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()
        OpinionFactory(content_object=utility)
        OpinionFactory(content_object=utility)

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()
        OpinionFactory(content_object=utility)
        OpinionFactory(content_object=utility)
        OpinionFactory(content_object=utility)

        self.assertEqual(self.category.get_total_count_opinions(), 6)

    def test_get_total_mark_if_has_attribute_total_mark(self):

        self.category.total_mark = 325466
        self.assertEqual(self.category.get_total_mark(), 325466)
        del self.category.total_mark

    def test_get_total_mark_if_no_utilities(self):

        self.assertEqual(self.category.get_total_mark(), 0)

    def test_get_total_mark_if_has_utilities_without_opinions(self):

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()
        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()

        self.assertEqual(self.category.get_total_mark(), 0)

    def test_get_total_mark_if_has_utility_with_good_opinion(self):

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()
        OpinionFactory(content_object=utility, is_useful=True, user=self.active_superuser)

        self.assertEqual(self.category.get_total_mark(), 1)

    def test_get_total_mark_if_has_utility_with_bad_opinion(self):

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()
        OpinionFactory(content_object=utility, is_useful=False, user=self.active_superuser)

        self.assertEqual(self.category.get_total_mark(), -1)

    def test_get_total_mark_if_has_utilities_with_equal_count_good_and_bad_opinions(self):

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()
        OpinionFactory(content_object=utility, is_useful=False, user=self.active_superuser)
        OpinionFactory(content_object=utility, is_useful=True, user=self.user2)
        OpinionFactory(content_object=utility, is_useful=True, user=self.user3)

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()
        OpinionFactory(content_object=utility, is_useful=False, user=self.active_superuser)
        OpinionFactory(content_object=utility, is_useful=True, user=self.user3)

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()
        OpinionFactory(content_object=utility, is_useful=True, user=self.user2)
        OpinionFactory(content_object=utility, is_useful=False, user=self.user3)
        OpinionFactory(content_object=utility, is_useful=False, user=self.user4)

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()

        self.assertEqual(self.category.get_total_mark(), 0)

    def test_get_total_mark_if_has_utilities_where_count_good_is_more_than_count_bad_opinions(self):

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()
        OpinionFactory(content_object=utility, is_useful=False, user=self.active_superuser)
        OpinionFactory(content_object=utility, is_useful=True, user=self.user2)
        OpinionFactory(content_object=utility, is_useful=False, user=self.user3)

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()
        OpinionFactory(content_object=utility, is_useful=True, user=self.active_superuser)
        OpinionFactory(content_object=utility, is_useful=True, user=self.user2)
        OpinionFactory(content_object=utility, is_useful=True, user=self.user3)

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()
        OpinionFactory(content_object=utility, is_useful=True, user=self.user2)
        OpinionFactory(content_object=utility, is_useful=True, user=self.user3)

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()
        OpinionFactory(content_object=utility, is_useful=True, user=self.user2)
        OpinionFactory(content_object=utility, is_useful=False, user=self.user4)
        OpinionFactory(content_object=utility, is_useful=True, user=self.user5)

        self.assertEqual(self.category.get_total_mark(), 5)

    def test_get_total_mark_if_has_utilities_where_count_good_is_less_than_count_bad_opinions(self):

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()
        OpinionFactory(content_object=utility, is_useful=True, user=self.active_superuser)
        OpinionFactory(content_object=utility, is_useful=False, user=self.user2)
        OpinionFactory(content_object=utility, is_useful=True, user=self.user3)

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()
        OpinionFactory(content_object=utility, is_useful=False, user=self.active_superuser)
        OpinionFactory(content_object=utility, is_useful=False, user=self.user2)
        OpinionFactory(content_object=utility, is_useful=False, user=self.user3)

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()
        OpinionFactory(content_object=utility, is_useful=False, user=self.user2)
        OpinionFactory(content_object=utility, is_useful=False, user=self.user3)

        utility = UtilityFactory(category=self.category)
        utility.opinions.clear()
        OpinionFactory(content_object=utility, is_useful=False, user=self.user2)
        OpinionFactory(content_object=utility, is_useful=True, user=self.user4)
        OpinionFactory(content_object=utility, is_useful=False, user=self.user5)

        self.assertEqual(self.category.get_total_mark(), -5)


class UtilityTests(EnhancedTestCase):

    @classmethod
    def setUpTestData(cls):

        cls.call_command('factory_test_users', '9')
        cls.call_command('factory_test_categories_of_utilities', '3')

        cls.category1, cls.category2, cls.category3 = UtilityCategory.objects.all()

        cls.user1, cls.user2, cls.user3, cls.user4, cls.user5 =\
            cls.django_user_model._default_manager.all()[:5]

        cls.utility = UtilityFactory(name='Universal app - GoldenDict', category=cls.category1)

        cls.utility.comments.clear()
        cls.utility.opinions.clear()

    def setUp(self):

        self.utility.refresh_from_db()

    def test_create_utility(self):

        data = {
            'name': 'Sublime Text 3',
            'description': """
                Mocha allows you to use any assertion library you wish.
                In the above example, we’re using Node.js’ built-in assert module–but generally,
                if it throws an Error, it will work! This means you can use libraries such as:
            """,
            'category': self.category1,
            'web_link': 'http://sublime-text-3.com'
        }

        utility = Utility(**data)
        utility.full_clean()
        utility.save()

        self.assertEqual(utility.name, data['name'])
        self.assertEqual(utility.description, data['description'])
        self.assertEqual(utility.category, data['category'])
        self.assertEqual(utility.web_link, data['web_link'])

    def test_update_utility(self):

        data = {
            'name': 'DevDoc.IO Chrome Extension',
            'description': """
                DevDocs combines multiple API documentations in a fast,
                organized, and searchable interface.
                Created and maintained by Thibaut Courouble
                Free and open source
                To keep up-to-date with the latest news:
                Follow @DevDocs on Twitter
                Watch the repository on GitHub
                Join the mailing list
            """,
            'category': self.category2,
            'web_link': 'http://devdocs.io/',
        }

        self.assertNotEqual(self.utility.name, data['name'])
        self.assertNotEqual(self.utility.description, data['description'])
        self.assertNotEqual(self.utility.category, data['category'])
        self.assertNotEqual(self.utility.web_link, data['web_link'])

        self.utility.name = data['name']
        self.utility.description = data['description']
        self.utility.category = data['category']
        self.utility.web_link = data['web_link']

        self.utility.full_clean()
        self.utility.save()

        self.assertEqual(self.utility.name, data['name'])
        self.assertEqual(self.utility.description, data['description'])
        self.assertEqual(self.utility.category, data['category'])
        self.assertEqual(self.utility.web_link, data['web_link'])

    def test_delete_utility(self):

        utility = UtilityFactory()
        utility.delete()

        with self.assertRaises(utility.DoesNotExist):
            utility.refresh_from_db()

    def test_str(self):
        self.assertEqual(str(self.utility), 'Universal app - GoldenDict')

    def test_get_count_comments_if_has_attribute_count_comments(self):

        self.utility.count_comments = 545214
        self.assertEqual(self.utility.get_count_comments(), 545214)
        del self.utility.count_comments

    def test_get_count_comments_if_no_comments(self):

        self.assertEqual(self.utility.get_count_comments(), 0)

    def test_get_count_comments_if_has_comment(self):

        CommentFactory(content_object=self.utility)
        self.assertEqual(self.utility.get_count_comments(), 1)

    def test_get_count_comments_if_has_comments(self):

        CommentFactory(content_object=self.utility)
        CommentFactory(content_object=self.utility)
        self.assertEqual(self.utility.get_count_comments(), 2)

    def test_get_count_opinions_if_has_attribute_count_opinions(self):

        self.utility.count_opinions = 782595
        self.assertEqual(self.utility.get_count_opinions(), 782595)
        del self.utility.count_opinions

    def test_get_count_opinions_if_has_no_opinions(self):

        self.assertEqual(self.utility.get_count_opinions(), 0)

    def test_get_count_opinions_if_has_opinion(self):

        OpinionFactory(content_object=self.utility)
        self.assertEqual(self.utility.get_count_opinions(), 1)

    def test_get_count_opinions_if_has_opinions(self):

        OpinionFactory(content_object=self.utility)
        OpinionFactory(content_object=self.utility)
        self.assertEqual(self.utility.get_count_opinions(), 2)

    def test_get_mark_if_has_attribute_mark(self):

        self.utility.mark = 98924
        self.assertEqual(self.utility.get_mark(), 98924)
        del self.utility.mark

    def test_get_mark_if_has_no_opinions(self):

        self.assertIsNone(self.utility.get_mark(), None)

    def test_get_mark_if_has_one_good_opinion(self):

        OpinionFactory(content_object=self.utility, is_useful=True, user=self.user1)
        self.assertEqual(self.utility.get_mark(), 1)

    def test_get_mark_if_has_one_bad_opinion(self):

        OpinionFactory(content_object=self.utility, is_useful=False, user=self.user1)
        self.assertEqual(self.utility.get_mark(), -1)

    def test_get_mark_if_has_equal_count_good_and_bad_opinions(self):

        OpinionFactory(content_object=self.utility, is_useful=False, user=self.user1)
        OpinionFactory(content_object=self.utility, is_useful=True, user=self.user2)
        OpinionFactory(content_object=self.utility, is_useful=False, user=self.user3)
        OpinionFactory(content_object=self.utility, is_useful=True, user=self.user4)
        self.assertEqual(self.utility.get_mark(), 0)

    def test_get_mark_if_has_more_count_good_than_bad_opinions(self):

        OpinionFactory(content_object=self.utility, is_useful=True, user=self.user1)
        OpinionFactory(content_object=self.utility, is_useful=True, user=self.user2)
        OpinionFactory(content_object=self.utility, is_useful=False, user=self.user3)
        OpinionFactory(content_object=self.utility, is_useful=True, user=self.user4)
        OpinionFactory(content_object=self.utility, is_useful=True, user=self.user5)
        self.assertEqual(self.utility.get_mark(), 3)

    def test_get_mark_if_has_less_count_good_than_bad_opinions(self):

        OpinionFactory(content_object=self.utility, is_useful=False, user=self.user1)
        OpinionFactory(content_object=self.utility, is_useful=True, user=self.user2)
        OpinionFactory(content_object=self.utility, is_useful=False, user=self.user3)
        OpinionFactory(content_object=self.utility, is_useful=False, user=self.user4)
        OpinionFactory(content_object=self.utility, is_useful=False, user=self.user5)
        self.assertEqual(self.utility.get_mark(), -3)
