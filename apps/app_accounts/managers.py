
import itertools
import collections

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    """
    Custom manager for custom auth model
    """

    def create_user(self, email, username, date_birthday, password=None):
        """Create staff user with certain attributes."""

        if not (email, username, date_birthday):
            raise ValueError(_('User must be have email, first name and last name.'))
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            date_birthday=date_birthday,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, date_birthday, password):
        """Creating superuser with certain attributes."""

        user = self.create_user(
            email=email,
            username=username,
            date_birthday=date_birthday,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_filled_accounts_profiles(self, accounts=None):
        """Return in percents, how many filled profiles of accounts information."""

        result = dict()
        list_restictions = (
                self.exclude(presents_on_stackoverflow='').values_list('pk', flat=True),
                self.exclude(personal_website='').values_list('pk', flat=True),
                self.exclude(presents_on_github='').values_list('pk', flat=True),
                self.exclude(presents_on_gmail='').values_list('pk', flat=True),
                self.filter(gender__isnull=False).values_list('pk', flat=True),
                self.exclude(real_name='').values_list('pk', flat=True),
        )
        counter = collections.Counter(
            itertools.chain(*list_restictions)
        )
        for pk, value in counter.items():
            result[pk] = 100 / len(list_restictions) * value
        return result
