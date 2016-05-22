
import unittest
import datetime

from mylabour import utils


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


if __name__ == '__main__':
    unittest.main()
