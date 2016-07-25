
import itertools
import collections

# from django.db import models
# from django.utils.translation import ugettext as _
from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    """
    Custom manager for custom auth model - Account.
    """

    def create_user(self, email, username, date_birthday, password):
        """Create staff user with certain attributes."""

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

    def get_filled_accounts_profiles(self, queryset=None):
        """Return in percents, how many filled profiles of accounts information.
        If given queryset, then using its as restriction for selection."""

        result = dict()
        # if queryset is none, then using all instances of models
        if queryset is None:
            queryset = self
        # listing restrictions determinating filled profile of account
        list_restictions = (
            queryset.exclude(presents_on_stackoverflow='').values_list('pk', flat=True),
            queryset.exclude(personal_website='').values_list('pk', flat=True),
            queryset.exclude(presents_on_github='').values_list('pk', flat=True),
            queryset.exclude(presents_on_gmail='').values_list('pk', flat=True),
            queryset.filter(gender__isnull=False).values_list('pk', flat=True),
            queryset.exclude(real_name='').values_list('pk', flat=True),
        )
        # counter all suitable instances
        counter = collections.Counter(
            itertools.chain(*list_restictions)
        )
        # determinating percent filled profile of account
        for pk, value in counter.items():
            result[pk] = 100 / len(list_restictions) * value
        # return as dictioinary {instance.pk: percent}
        return result
