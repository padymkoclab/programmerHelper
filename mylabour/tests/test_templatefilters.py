
import unittest
from datetime import timedelta

from django.utils import timezone

from .templatetags import myfilters


class Test_UpDownChars(unittest.TestCase):
    """

    """

    def test_results(self):
        self.assertEqual(myfilters.UpDownChars('asasasas'), 'AsAsAsAs')
        self.assertEqual(myfilters.UpDownChars('fsafn jkd jfjsad ks'), 'FsAfN JkD JfJsAd kS')
        self.assertEqual(myfilters.UpDownChars('ADDSDD'), 'AdDsDd')
        self.assertEqual(myfilters.UpDownChars('Ax'), 'Ax')
        self.assertEqual(myfilters.UpDownChars('aXx'), 'AxX')


class Test_FormattingBigNumber(unittest.TestCase):
    """

    """

    def test_without_value_for_paraments(self):
        self.assertEqual(myfilters.FormattingBigNumber(2414121421), '2 414 121 421')
        self.assertEqual(myfilters.FormattingBigNumber(451), '451')

    def test_with_another_value_for_count_digits_in_block(self):
        self.assertEqual(myfilters.FormattingBigNumber(4233342342, paraments=' &3'), '4 233 342 342')
        self.assertEqual(myfilters.FormattingBigNumber(12456, paraments=' &4'), '1 2456')
        self.assertEqual(myfilters.FormattingBigNumber(4548152233, paraments=' &2'), '45 48 15 22 33')

    def test_with_another_separator(self):
        self.assertEqual(myfilters.FormattingBigNumber(54545122, paraments='.&3'), '54.545.122')
        self.assertEqual(myfilters.FormattingBigNumber(45684315616, paraments='#&4'), '456#8431#5616')
        self.assertEqual(myfilters.FormattingBigNumber(78831215, paraments=',&2'), '78,83,12,15')


class Test_DisplayLastSortedByField(unittest.TestCase):
    """

    """

    def setUp(self):

        class A():

            def __init__(self, x, y):
                self.x = x
                self.y = y

            def __repr__(self):
                return 'A(x={0.x}, y={0.y})'.format(self)

        self.list_objects = [
            A(x=-4, y=3),
            A(x=-44, y=1),
            A(x=14, y=6),
            A(x=42, y=-4),
            A(x=41, y=31),
            A(x=12, y=1),
            A(x=-78, y=-31),
            A(x=30, y=11),
        ]
        self.class_A = A

    def test_without_list_objects(self):
        self.assertEqual(myfilters.DisplayLastSortedByField([], 'field_name'), [])

    def test_list_objects_without_field_for_sort(self):
        self.assertRaises(AttributeError, myfilters.DisplayLastSortedByField, list_objects=self.list_objects, field_name='z')

    def test_return_only_5_elements_of_sequence(self):
        self.assertEqual(len(myfilters.DisplayLastSortedByField(self.list_objects, 'x')), 5)

    def test_return_elements_of_sequence_in_ordered(self):
        list_ordered_by_field = myfilters.DisplayLastSortedByField(self.list_objects, 'x')
        # sorting current list
        self.list_objects.sort(key=lambda el: el.x, reverse=True)
        self.assertListEqual(list_ordered_by_field, self.list_objects[:5])


class Test_DisplayRandomElements(unittest.TestCase):
    """

    """

    def setUp(self):
        self.list_objects = [1, 243, 434, 545, 3454, 54, 54, 545, 45]

    def test_return_random_list_objects_by_determinated_count_random_element(self):
        self.assertEqual(len(myfilters.DisplayRandomElements(self.list_objects)), 5)
        self.assertEqual(len(myfilters.DisplayRandomElements(self.list_objects, 3)), 3)
        self.assertEqual(len(myfilters.DisplayRandomElements(self.list_objects, 7)), 7)

    def test_if_count_random_element_is_less_then_count_list_objects(self):
        self.assertEqual(len(myfilters.DisplayRandomElements(self.list_objects[:3])), 3)


class Test_HighlightFoundedText(unittest.TestCase):
    """

    """

    def test_is_founded_text_for_highlight(self):
        self.assertEqual(
            myfilters.HighlightFoundedText('import django', 'django'),
            'import <span class=\'highlight_founded_text\'>django</span>'
        )
        self.assertEqual(
            myfilters.HighlightFoundedText('class Simple(object):', 'CLASS'),
            '<span class=\'highlight_founded_text\'>class</span> Simple(object):'
        )

    def test_is_not_founded_text_for_highlight(self):
        self.assertEqual(myfilters.HighlightFoundedText('console.info(vegatetion)', 'view'), 'console.info(vegatetion)')
        self.assertEqual(myfilters.HighlightFoundedText('$(\'body\').hide()', 'hidden'), '$(\'body\').hide()')


class Test_CountTimeExistence(unittest.TestCase):
    """

    """

    def setUp(self):
        self.now = timezone.now()
        self.datetime1 = timezone.now() - timedelta(days=1)
        self.datetime2 = timezone.now() - timedelta(days=2)
        self.datetime3 = timezone.now() - timedelta(days=31)
        self.datetime4 = timezone.now() - timedelta(days=200)
        self.datetime5 = timezone.now() - timedelta(days=256)
        self.datetime6 = timezone.now() - timedelta(days=400)
        self.datetime7 = timezone.datetime(2000, 12, 18, tzinfo=self.now.tzinfo)
        self.datetime8 = timezone.datetime(1890, 12, 31, tzinfo=self.now.tzinfo)
        self.datetime9 = timezone.datetime(1950, 7, 11, tzinfo=self.now.tzinfo)

    def test_if_datetime_is_past(self):
        self.assertEqual(myfilters.CountTimeExistence(self.datetime1), 2)
        self.assertEqual(myfilters.CountTimeExistence(self.datetime2), 3)
        self.assertEqual(myfilters.CountTimeExistence(self.datetime3), 32)
        self.assertEqual(myfilters.CountTimeExistence(self.datetime4), 201)
        self.assertEqual(myfilters.CountTimeExistence(self.datetime5), 257)
        self.assertEqual(myfilters.CountTimeExistence(self.datetime6), 401)

    def test_if_datetime_is_now(self):
        self.assertEqual(myfilters.CountTimeExistence(self.now), 1)

    def test_if_datetime_in_future(self):
        self.assertRaises(ValueError, myfilters.CountTimeExistence, self.now + timedelta(days=18))
        self.assertRaises(ValueError, myfilters.CountTimeExistence, self.now + timedelta(days=1))


class Test_DisplaySingNumber(unittest.TestCase):
    """

    """

    def test_if_value_is_0(self):
        self.assertEqual(myfilters.DisplaySingNumber(0), 0)

    def test_if_value_is_negative_number(self):
        self.assertEqual(myfilters.DisplaySingNumber(-345488), '-345488')

    def test_if_value_is_positive_number(self):
        self.assertEqual(myfilters.DisplaySingNumber(4524), '+4524')
