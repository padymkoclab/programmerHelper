
from django.utils.translation import ugettext as _
from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    """
    Custom manager for custom auth model
    """

    def create_user(self, email, username, date_birthday, password=None):
        """
        Create staff user
        """

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
        user = self.create_user(
            email=email,
            username=username,
            date_birthday=date_birthday,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user
