
from django.core.management.base import CommandError

from mylabour.test_utils import EnhancedTestCase

from apps.utilities.models import UtilityCategory, Utility


class FactoryTestCategoriesOfUtilitiesTests(EnhancedTestCase):

    def test_attempt_factory_count_objects_less_0(self):

        with self.assertRaisesMessage(
            CommandError,
            'Error: argument count: Count must be integer in range from 1 to 999 (passed -1)'
        ):
            self.call_command('factory_test_categories_utilities', '-1')

    def test_attempt_factory_0_objects(self):

        with self.assertRaisesMessage(
            CommandError,
            'Error: argument count: Count must be integer in range from 1 to 999 (passed 0)'
        ):
            self.call_command('factory_test_categories_utilities', '0')

    def test_factory_1_object(self):

        self.call_command('factory_test_categories_utilities', '1')
        self.assertEqual(UtilityCategory.objects.count(), 1)

    def test_factory_2_objects(self):

        self.call_command('factory_test_categories_utilities', '2')
        self.assertEqual(UtilityCategory.objects.count(), 2)

    def test_factory_10_objects(self):

        self.call_command('factory_test_categories_utilities', '10')
        self.assertEqual(UtilityCategory.objects.count(), 10)

    def test_factory_objects_if_objects_exists(self):

        self.call_command('factory_test_categories_utilities', '4')
        self.assertEqual(UtilityCategory.objects.count(), 4)

        self.call_command('factory_test_categories_utilities', '5')
        self.assertEqual(UtilityCategory.objects.count(), 5)

        self.call_command('factory_test_categories_utilities', '2')
        self.assertEqual(UtilityCategory.objects.count(), 2)


class FactoryTestUtilitiesTests(EnhancedTestCase):

    @classmethod
    def setUpTestData(cls):

        cls.call_command('factory_test_users', '10')
        cls.call_command('factory_test_categories_utilities', '3')

    def test_attempt_factory_count_objects_less_0(self):

        with self.assertRaisesMessage(
            CommandError,
            'Error: argument count: Count must be integer in range from 1 to 999 (passed -1)'
        ):
            self.call_command('factory_test_utilities', '-1')

    def test_attempt_factory_0_objects(self):

        with self.assertRaisesMessage(
            CommandError,
            'Error: argument count: Count must be integer in range from 1 to 999 (passed 0)'
        ):
            self.call_command('factory_test_utilities', '0')

    def test_factory_1_object(self):

        self.call_command('factory_test_utilities', '1')
        self.assertEqual(Utility.objects.count(), 1)

    def test_factory_2_objects(self):

        self.call_command('factory_test_utilities', '2')
        self.assertEqual(Utility.objects.count(), 2)

    def test_factory_10_objects(self):

        self.call_command('factory_test_utilities', '10')
        self.assertEqual(Utility.objects.count(), 10)

    def test_factory_objects_if_objects_exists(self):

        self.call_command('factory_test_utilities', '4')
        self.assertEqual(Utility.objects.count(), 4)

        self.call_command('factory_test_utilities', '5')
        self.assertEqual(Utility.objects.count(), 5)

        self.call_command('factory_test_utilities', '2')
        self.assertEqual(Utility.objects.count(), 2)
