
import unittest

from django.core.exceptions import ValidationError

from .validators import Validator_UserName


class Test_Validator_UserName(unittest.TestCase):
    """
    Testing validator Validator_UserName
    """

    def test_with_chars_in_uppercase(self):
        self.assertRaises(ValidationError, Validator_UserName, 'fhajbsaA')
        self.assertRaises(ValidationError, Validator_UserName, 'fhajbsaA')
        self.assertRaises(ValidationError, Validator_UserName, 'AS_Dhsbdhsb_ASA')

    def test_with_non_ascii_chars(self):
        self.assertRaises(ValidationError, Validator_UserName, 'раоіsdsdsAфроиіф')
        self.assertRaises(ValidationError, Validator_UserName, 'Aфроиіф')
        self.assertRaises(ValidationError, Validator_UserName, 'AdsdasВірирі')

    def test_where_all_chars_is_digits(self):
        self.assertRaises(ValidationError, Validator_UserName, '454785454')
        self.assertRaises(ValidationError, Validator_UserName, '1')
        self.assertRaises(ValidationError, Validator_UserName, '0000000')
