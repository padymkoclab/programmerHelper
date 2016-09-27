
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django import forms


class LoginForm(forms.Form):
    """ """

    credential = forms.CharField(
        label=_('Email or username'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter username or email'),
            'class': 'form-control',
            'autofocus': '',
        }),
        strip=True,
        help_text=_('Field is case-sensetive'),
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Enter password'),
            'class': 'form-control',
        }),
        strip=False,
    )

    error_messages = {
        'invalid_login': _('Please enter a correct credentials for login.'),
        'inactive': _('This user is inactive.'),
    }

    def __init__(self, *args, **kwargs):

        # for keeping trying authentication of an user
        self.user = None

        super().__init__(*args, **kwargs)

    def clean(self):

        credential = self.cleaned_data.get('credential')
        password = self.cleaned_data.get('password')

        if credential and password:
            user = authenticate(credential=credential, password=password)

            if user is None:
                raise forms.ValidationError(self.error_messages['invalid_login'], code='invalid_login')

            if not user.is_active:
                raise forms.ValidationError(self.error_messages['inactive'], code='inactive')

            # keep a active and authenticated of an user
            self.user = user

        return self.cleaned_data

    def get_user(self):
        """ """

        return self.user


class LogoutForm(forms.Form):

    pass
