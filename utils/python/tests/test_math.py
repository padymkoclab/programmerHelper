
import unittest

import pytest

from ..math import count_combinations


class MathTest(unittest.TestCase):

    def test_count_combinations(self):
        assert count_combinations(15, 4) == 1365
        assert count_combinations(52, 5) == 2598960
        assert count_combinations(15, 8) == 6435
        assert count_combinations(255, 14) == 39206761937327465798625
        assert count_combinations(78, 3) == 76076
        assert count_combinations(4, 4) == 1
        assert count_combinations(6, 5) == 1
        assert count_combinations(9, 5) == 1
        assert count_combinations(10, 5) == 2
        assert count_combinations(10, 0) == 0
        assert count_combinations(0, 0) == 0
        assert count_combinations(1000, 10) == 263409560461970212832400

    def test_count_combinations_error(self):

        with pytest.raises(ValueError):
            count_combinations(5, 7)
        with pytest.raises(TypeError):
            count_combinations(6, None)
        with pytest.raises(TypeError):
            count_combinations(6, True)
        with pytest.raises(TypeError):
            count_combinations(None, [])
        with pytest.raises(TypeError):
            count_combinations(None, None)
        with pytest.raises(TypeError):
            count_combinations(True, False)
