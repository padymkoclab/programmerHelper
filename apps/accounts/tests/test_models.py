
import unittest
import datetime

from django.test import TestCase

# from apps.accounts.factories import fillup_models_accounts_data
from apps.accounts.models import Account


@unittest.skip('reason')
class AccountTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        fillup_models_accounts_data()

    def test_the_method_have_certain_count_consecutive_days(self):
        account = Account.objects.random_objects(1).get()
        self.assertFalse(account.have_certain_count_consecutive_days(1))
        account.days_attendances.create(day_attendance=datetime.date(2016, 4, 4))
        account.days_attendances.create(day_attendance=datetime.date(2016, 4, 5))
        account.days_attendances.create(day_attendance=datetime.date(2016, 4, 6))
        account.days_attendances.create(day_attendance=datetime.date(2016, 4, 7))
        self.assertFalse(account.have_certain_count_consecutive_days(5))
        self.assertTrue(account.have_certain_count_consecutive_days(4))
        self.assertTrue(account.have_certain_count_consecutive_days(1))
