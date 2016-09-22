
import itertools
import collections

from django.db import models
# from django.utils.translation import ugettext as _
from django.contrib.auth.models import BaseUserManager

from .querysets import LevelQuerySet, UserQuerySet


class LevelManager(models.Manager):

    pass


LevelManager = LevelManager.from_queryset(LevelQuerySet)


class UserManager(BaseUserManager):
    """
    Custom manager for custom user model
    """

    def create_user(self, email, username, password, display_name):
        """Create staff user with certain attributes."""

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            display_name=display_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, display_name):
        """Creating superuser with certain attributes."""

        user = self.create_user(
            email=email,
            username=username,
            password=password,
            display_name=display_name,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_filled_users_profiles(self, queryset=None):
        """Return in percents, how many filled profiles of users information.
        If given queryset, then using its as restriction for selection."""

        result = dict()
        # if queryset is none, then using all instances of models
        if queryset is None:
            queryset = self
        # listing restrictions determinating filled profile of user
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
        # determinating percent filled profile of user
        for pk, value in counter.items():
            result[pk] = 100 / len(list_restictions) * value
        # return as dictioinary {instance.pk: percent}
        return result


UserManager = UserManager.from_queryset(UserQuerySet)


class ActiveUserManager(models.Manager):
    """ """

    pass
