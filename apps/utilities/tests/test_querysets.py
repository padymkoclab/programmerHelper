
from utils.django.test_utils import EnhancedTestCase

from apps.comments.factories import CommentFactory
from apps.opinions.factories import OpinionFactory
from apps.utilities.models import UtilityCategory, Utility
from apps.utilities.factories import UtilityFactory, UtilityCategoryFactory


class UtilityCategoryQuerySetTests(EnhancedTestCase):

    @classmethod
    def setUpTestData(cls):

        cls.call_command('factory_test_users', '10')

        cls.category1 = UtilityCategoryFactory()

        cls.category2 = UtilityCategoryFactory()
        cls.utility1 = UtilityFactory(category=cls.category2)

        cls.category3 = UtilityCategoryFactory()
        cls.utility2 = UtilityFactory(category=cls.category3)
        cls.utility3 = UtilityFactory(category=cls.category3)

        cls.category4 = UtilityCategoryFactory()
        cls.utility4 = UtilityFactory(category=cls.category4)
        cls.utility5 = UtilityFactory(category=cls.category4)
        cls.utility6 = UtilityFactory(category=cls.category4)

        cls.category5 = UtilityCategoryFactory()
        cls.utility7 = UtilityFactory(category=cls.category5)
        cls.utility8 = UtilityFactory(category=cls.category5)
        cls.utility9 = UtilityFactory(category=cls.category5)
        cls.utility10 = UtilityFactory(category=cls.category5)

        cls.category6 = UtilityCategoryFactory()
        cls.utility11 = UtilityFactory(category=cls.category6)
        cls.utility12 = UtilityFactory(category=cls.category6)
        cls.utility13 = UtilityFactory(category=cls.category6)
        cls.utility14 = UtilityFactory(category=cls.category6)
        cls.utility15 = UtilityFactory(category=cls.category6)

        for utility in Utility.objects.all():
            utility.opinions.clear()
            utility.comments.clear()

        CommentFactory(content_object=cls.utility2)

        OpinionFactory(content_object=cls.utility3, is_useful=True)

        CommentFactory(content_object=cls.utility4)
        OpinionFactory(content_object=cls.utility4, is_useful=False)

        CommentFactory(content_object=cls.utility5)
        CommentFactory(content_object=cls.utility5)
        OpinionFactory(content_object=cls.utility5, is_useful=False)
        OpinionFactory(content_object=cls.utility5, is_useful=True)
        OpinionFactory(content_object=cls.utility5, is_useful=True)

        CommentFactory(content_object=cls.utility6)
        CommentFactory(content_object=cls.utility6)
        OpinionFactory(content_object=cls.utility6, is_useful=True)
        OpinionFactory(content_object=cls.utility6, is_useful=True)
        OpinionFactory(content_object=cls.utility6, is_useful=True)
        OpinionFactory(content_object=cls.utility6, is_useful=True)

        CommentFactory(content_object=cls.utility7)
        CommentFactory(content_object=cls.utility7)
        OpinionFactory(content_object=cls.utility7, is_useful=False)
        OpinionFactory(content_object=cls.utility7, is_useful=False)

        CommentFactory(content_object=cls.utility8)
        CommentFactory(content_object=cls.utility8)
        CommentFactory(content_object=cls.utility8)
        CommentFactory(content_object=cls.utility8)
        OpinionFactory(content_object=cls.utility8, is_useful=False)
        OpinionFactory(content_object=cls.utility8, is_useful=False)
        OpinionFactory(content_object=cls.utility8, is_useful=False)
        OpinionFactory(content_object=cls.utility8, is_useful=False)

        CommentFactory(content_object=cls.utility9)
        CommentFactory(content_object=cls.utility9)
        CommentFactory(content_object=cls.utility9)
        CommentFactory(content_object=cls.utility9)
        OpinionFactory(content_object=cls.utility9, is_useful=True)
        OpinionFactory(content_object=cls.utility9, is_useful=True)
        OpinionFactory(content_object=cls.utility9, is_useful=True)
        OpinionFactory(content_object=cls.utility9, is_useful=True)

        OpinionFactory(content_object=cls.utility10, is_useful=False)
        OpinionFactory(content_object=cls.utility10, is_useful=True)
        OpinionFactory(content_object=cls.utility10, is_useful=True)
        OpinionFactory(content_object=cls.utility10, is_useful=True)

        OpinionFactory(content_object=cls.utility11, is_useful=True)
        OpinionFactory(content_object=cls.utility11, is_useful=False)
        OpinionFactory(content_object=cls.utility11, is_useful=False)
        OpinionFactory(content_object=cls.utility11, is_useful=False)
        OpinionFactory(content_object=cls.utility11, is_useful=False)

        CommentFactory(content_object=cls.utility12)
        CommentFactory(content_object=cls.utility12)
        CommentFactory(content_object=cls.utility12)
        CommentFactory(content_object=cls.utility12)

        OpinionFactory(content_object=cls.utility13, is_useful=False)
        OpinionFactory(content_object=cls.utility13, is_useful=False)
        OpinionFactory(content_object=cls.utility13, is_useful=False)
        OpinionFactory(content_object=cls.utility13, is_useful=False)
        OpinionFactory(content_object=cls.utility13, is_useful=False)
        OpinionFactory(content_object=cls.utility13, is_useful=False)
        CommentFactory(content_object=cls.utility13)
        CommentFactory(content_object=cls.utility13)
        CommentFactory(content_object=cls.utility13)
        CommentFactory(content_object=cls.utility13)
        CommentFactory(content_object=cls.utility13)
        CommentFactory(content_object=cls.utility13)

        OpinionFactory(content_object=cls.utility14, is_useful=True)
        OpinionFactory(content_object=cls.utility14, is_useful=True)
        OpinionFactory(content_object=cls.utility14, is_useful=True)
        OpinionFactory(content_object=cls.utility14, is_useful=True)
        OpinionFactory(content_object=cls.utility14, is_useful=True)
        OpinionFactory(content_object=cls.utility14, is_useful=True)
        CommentFactory(content_object=cls.utility14)
        CommentFactory(content_object=cls.utility14)

    def test_categories_with_count_utilities(self):

        categories_with_count_utilities = UtilityCategory.objects.categories_with_count_utilities()
        values = categories_with_count_utilities.values('count_utilities')

        self.assertEqual(values.get(pk=self.category1.pk)['count_utilities'], 0)
        self.assertEqual(values.get(pk=self.category2.pk)['count_utilities'], 1)
        self.assertEqual(values.get(pk=self.category3.pk)['count_utilities'], 2)
        self.assertEqual(values.get(pk=self.category4.pk)['count_utilities'], 3)
        self.assertEqual(values.get(pk=self.category5.pk)['count_utilities'], 4)
        self.assertEqual(values.get(pk=self.category6.pk)['count_utilities'], 5)

    def test_categories_with_total_count_opinions(self):

        categories_with_total_count_opinions = UtilityCategory.objects.categories_with_total_count_opinions()
        values = categories_with_total_count_opinions.values('total_count_opinions')

        self.assertEqual(values.get(pk=self.category1.pk)['total_count_opinions'], 0)
        self.assertEqual(values.get(pk=self.category2.pk)['total_count_opinions'], 0)
        self.assertEqual(values.get(pk=self.category3.pk)['total_count_opinions'], 1)
        self.assertEqual(values.get(pk=self.category4.pk)['total_count_opinions'], 8)
        self.assertEqual(values.get(pk=self.category5.pk)['total_count_opinions'], 14)
        self.assertEqual(values.get(pk=self.category6.pk)['total_count_opinions'], 17)

    def test_categories_with_total_count_comments(self):

        categories_with_total_count_comments = UtilityCategory.objects.categories_with_total_count_comments()
        values = categories_with_total_count_comments.values('total_count_comments')

        self.assertEqual(values.get(pk=self.category1.pk)['total_count_comments'], 0)
        self.assertEqual(values.get(pk=self.category2.pk)['total_count_comments'], 0)
        self.assertEqual(values.get(pk=self.category3.pk)['total_count_comments'], 1)
        self.assertEqual(values.get(pk=self.category4.pk)['total_count_comments'], 5)
        self.assertEqual(values.get(pk=self.category5.pk)['total_count_comments'], 10)
        self.assertEqual(values.get(pk=self.category6.pk)['total_count_comments'], 12)

    def test_categories_with_total_marks(self):

        categories_with_total_marks = UtilityCategory.objects.categories_with_total_marks()
        values = categories_with_total_marks.values('total_mark')

        self.assertIsNone(values.get(pk=self.category1.pk)['total_mark'])
        self.assertIsNone(values.get(pk=self.category2.pk)['total_mark'])
        self.assertEqual(values.get(pk=self.category3.pk)['total_mark'], 1)
        self.assertEqual(values.get(pk=self.category4.pk)['total_mark'], 4)
        self.assertEqual(values.get(pk=self.category5.pk)['total_mark'], 0)
        self.assertEqual(values.get(pk=self.category6.pk)['total_mark'], -3)

    def test_categories_with_all_additional_fields(self):

        categories_with_all_additional_fields = UtilityCategory.objects.categories_with_all_additional_fields()
        values = categories_with_all_additional_fields.values(
            'count_utilities', 'total_count_opinions', 'total_count_comments', 'total_mark',
        )

        self.assertEqual(values.get(pk=self.category1.pk)['count_utilities'], 0)
        self.assertEqual(values.get(pk=self.category2.pk)['count_utilities'], 1)
        self.assertEqual(values.get(pk=self.category3.pk)['count_utilities'], 2)
        self.assertEqual(values.get(pk=self.category4.pk)['count_utilities'], 3)
        self.assertEqual(values.get(pk=self.category5.pk)['count_utilities'], 4)
        self.assertEqual(values.get(pk=self.category6.pk)['count_utilities'], 5)

        self.assertEqual(values.get(pk=self.category1.pk)['total_count_opinions'], 0)
        self.assertEqual(values.get(pk=self.category2.pk)['total_count_opinions'], 0)
        self.assertEqual(values.get(pk=self.category3.pk)['total_count_opinions'], 1)
        self.assertEqual(values.get(pk=self.category4.pk)['total_count_opinions'], 8)
        self.assertEqual(values.get(pk=self.category5.pk)['total_count_opinions'], 14)
        self.assertEqual(values.get(pk=self.category6.pk)['total_count_opinions'], 17)

        self.assertEqual(values.get(pk=self.category1.pk)['total_count_comments'], 0)
        self.assertEqual(values.get(pk=self.category2.pk)['total_count_comments'], 0)
        self.assertEqual(values.get(pk=self.category3.pk)['total_count_comments'], 1)
        self.assertEqual(values.get(pk=self.category4.pk)['total_count_comments'], 5)
        self.assertEqual(values.get(pk=self.category5.pk)['total_count_comments'], 10)
        self.assertEqual(values.get(pk=self.category6.pk)['total_count_comments'], 12)

        self.assertIsNone(values.get(pk=self.category1.pk)['total_mark'])
        self.assertIsNone(values.get(pk=self.category2.pk)['total_mark'])
        self.assertEqual(values.get(pk=self.category3.pk)['total_mark'], 1)
        self.assertEqual(values.get(pk=self.category4.pk)['total_mark'], 4)
        self.assertEqual(values.get(pk=self.category5.pk)['total_mark'], 0)
        self.assertEqual(values.get(pk=self.category6.pk)['total_mark'], -3)


class UtilityQuerySetTests(EnhancedTestCase):

    @classmethod
    def setUpTestData(cls):

        cls.call_command('factory_test_users', '10')
        cls.call_command('factory_test_categories_utilities', '4')
        cls.call_command('factory_test_utilities', '9')

        for utility in Utility.objects.all():
            utility.opinions.clear()
            utility.comments.clear()

        cls.utility1, cls.utility2, cls.utility3, cls.utility4, cls.utility5,\
            cls.utility6, cls.utility7, cls.utility8, cls.utility9 = Utility.objects.all()

        CommentFactory(content_object=cls.utility2)

        OpinionFactory(content_object=cls.utility3, is_useful=True)

        CommentFactory(content_object=cls.utility4)
        OpinionFactory(content_object=cls.utility4, is_useful=False)

        CommentFactory(content_object=cls.utility5)
        CommentFactory(content_object=cls.utility5)
        OpinionFactory(content_object=cls.utility5, is_useful=False)
        OpinionFactory(content_object=cls.utility5, is_useful=True)

        CommentFactory(content_object=cls.utility6)
        CommentFactory(content_object=cls.utility6)
        OpinionFactory(content_object=cls.utility6, is_useful=True)
        OpinionFactory(content_object=cls.utility6, is_useful=True)

        CommentFactory(content_object=cls.utility7)
        CommentFactory(content_object=cls.utility7)
        OpinionFactory(content_object=cls.utility7, is_useful=False)
        OpinionFactory(content_object=cls.utility7, is_useful=False)

        CommentFactory(content_object=cls.utility8)
        CommentFactory(content_object=cls.utility8)
        CommentFactory(content_object=cls.utility8)
        CommentFactory(content_object=cls.utility8)
        OpinionFactory(content_object=cls.utility8, is_useful=False)
        OpinionFactory(content_object=cls.utility8, is_useful=False)
        OpinionFactory(content_object=cls.utility8, is_useful=False)
        OpinionFactory(content_object=cls.utility8, is_useful=False)

        CommentFactory(content_object=cls.utility9)
        CommentFactory(content_object=cls.utility9)
        CommentFactory(content_object=cls.utility9)
        CommentFactory(content_object=cls.utility9)
        OpinionFactory(content_object=cls.utility9, is_useful=True)
        OpinionFactory(content_object=cls.utility9, is_useful=True)
        OpinionFactory(content_object=cls.utility9, is_useful=True)
        OpinionFactory(content_object=cls.utility9, is_useful=True)

    def test_utilities_with_count_opinions(self):

        utilities_with_count_opinions = Utility.objects.utilities_with_count_opinions()
        values = utilities_with_count_opinions.values('count_opinions')

        self.assertEqual(values.get(pk=self.utility1.pk)['count_opinions'], 0)
        self.assertEqual(values.get(pk=self.utility2.pk)['count_opinions'], 0)
        self.assertEqual(values.get(pk=self.utility3.pk)['count_opinions'], 1)
        self.assertEqual(values.get(pk=self.utility4.pk)['count_opinions'], 1)
        self.assertEqual(values.get(pk=self.utility5.pk)['count_opinions'], 2)
        self.assertEqual(values.get(pk=self.utility6.pk)['count_opinions'], 2)
        self.assertEqual(values.get(pk=self.utility7.pk)['count_opinions'], 2)
        self.assertEqual(values.get(pk=self.utility8.pk)['count_opinions'], 4)
        self.assertEqual(values.get(pk=self.utility9.pk)['count_opinions'], 4)

    def test_utilities_with_count_comments(self):

        utilities_with_count_comments = Utility.objects.utilities_with_count_comments()
        values = utilities_with_count_comments.values('count_comments')

        self.assertEqual(values.get(pk=self.utility1.pk)['count_comments'], 0)
        self.assertEqual(values.get(pk=self.utility2.pk)['count_comments'], 1)
        self.assertEqual(values.get(pk=self.utility3.pk)['count_comments'], 0)
        self.assertEqual(values.get(pk=self.utility4.pk)['count_comments'], 1)
        self.assertEqual(values.get(pk=self.utility5.pk)['count_comments'], 2)
        self.assertEqual(values.get(pk=self.utility6.pk)['count_comments'], 2)
        self.assertEqual(values.get(pk=self.utility7.pk)['count_comments'], 2)
        self.assertEqual(values.get(pk=self.utility8.pk)['count_comments'], 4)
        self.assertEqual(values.get(pk=self.utility9.pk)['count_comments'], 4)

    def test_utilities_with_marks(self):

        utilities_with_marks = Utility.objects.utilities_with_marks()
        values = utilities_with_marks.values('mark')

        self.assertIsNone(values.get(pk=self.utility1.pk)['mark'])
        self.assertIsNone(values.get(pk=self.utility2.pk)['mark'])
        self.assertEqual(values.get(pk=self.utility3.pk)['mark'], 1)
        self.assertEqual(values.get(pk=self.utility4.pk)['mark'], -1)
        self.assertEqual(values.get(pk=self.utility5.pk)['mark'], 0)
        self.assertEqual(values.get(pk=self.utility6.pk)['mark'], 2)
        self.assertEqual(values.get(pk=self.utility7.pk)['mark'], -2)
        self.assertEqual(values.get(pk=self.utility8.pk)['mark'], -4)
        self.assertEqual(values.get(pk=self.utility9.pk)['mark'], 4)

    def test_utilities_with_all_additional_fields(self):

        utilities_with_all_additional_fields = Utility.objects.utilities_with_all_additional_fields()
        values = utilities_with_all_additional_fields.values('count_opinions', 'mark', 'count_comments')

        self.assertEqual(values.get(pk=self.utility1.pk)['count_opinions'], 0)
        self.assertEqual(values.get(pk=self.utility2.pk)['count_opinions'], 0)
        self.assertEqual(values.get(pk=self.utility3.pk)['count_opinions'], 1)
        self.assertEqual(values.get(pk=self.utility4.pk)['count_opinions'], 1)
        self.assertEqual(values.get(pk=self.utility5.pk)['count_opinions'], 2)
        self.assertEqual(values.get(pk=self.utility6.pk)['count_opinions'], 2)
        self.assertEqual(values.get(pk=self.utility7.pk)['count_opinions'], 2)
        self.assertEqual(values.get(pk=self.utility8.pk)['count_opinions'], 4)
        self.assertEqual(values.get(pk=self.utility9.pk)['count_opinions'], 4)

        self.assertEqual(values.get(pk=self.utility1.pk)['count_comments'], 0)
        self.assertEqual(values.get(pk=self.utility2.pk)['count_comments'], 1)
        self.assertEqual(values.get(pk=self.utility3.pk)['count_comments'], 0)
        self.assertEqual(values.get(pk=self.utility4.pk)['count_comments'], 1)
        self.assertEqual(values.get(pk=self.utility5.pk)['count_comments'], 2)
        self.assertEqual(values.get(pk=self.utility6.pk)['count_comments'], 2)
        self.assertEqual(values.get(pk=self.utility7.pk)['count_comments'], 2)
        self.assertEqual(values.get(pk=self.utility8.pk)['count_comments'], 4)
        self.assertEqual(values.get(pk=self.utility9.pk)['count_comments'], 4)

        self.assertIsNone(values.get(pk=self.utility1.pk)['mark'])
        self.assertIsNone(values.get(pk=self.utility2.pk)['mark'])
        self.assertEqual(values.get(pk=self.utility3.pk)['mark'], 1)
        self.assertEqual(values.get(pk=self.utility4.pk)['mark'], -1)
        self.assertEqual(values.get(pk=self.utility5.pk)['mark'], 0)
        self.assertEqual(values.get(pk=self.utility6.pk)['mark'], 2)
        self.assertEqual(values.get(pk=self.utility7.pk)['mark'], -2)
        self.assertEqual(values.get(pk=self.utility8.pk)['mark'], -4)
        self.assertEqual(values.get(pk=self.utility9.pk)['mark'], 4)
