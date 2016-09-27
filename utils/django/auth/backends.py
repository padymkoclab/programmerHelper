
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """
    Worked only if USERNAME_FIELD = ['email']
    """

    def authenticate(self, email=None, password=None, **kwargs):

        UserModel = get_user_model()

        if email is None:
            email = kwargs.get(UserModel.USERNAME_FIELD)

        try:
            user = UserModel._default_manager.get_by_natural_key(email=email)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
        else:

            # inactive users is non rejected
            if user.check_password(password):
                return user


class UsernameEmailBackend(ModelBackend):
    """
    A model must be have fields 'username' and 'email',
    """

    def authenticate(self, credential=None, password=None, **kwargs):

        UserModel = get_user_model()

        if credential is None:
            return

        field = 'email' if '@' in credential else 'username'

        try:
            user = UserModel._default_manager.get(**{field: credential})
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
        else:

            # inactive users is non rejected
            if user.check_password(password):
                return user
