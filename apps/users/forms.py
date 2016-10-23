
from django.utils.html import format_html
from django.utils.text import force_text
from django.contrib import postgres
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.conf import settings
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import password_validation

from utils.django import widgets as utils_widgets

from apps.admin.forms import AddChangeModelForm

# from passwords.fields import PasswordField
# from passwords.validators import (
#     DictionaryValidator, LengthValidator, ComplexityValidator)

from .models import User, Level


class UserCreateAdminModelForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['alias'].widget.attrs['class'] = 'span9'
        self.fields['alias'].widget.attrs['placeholder'] = _('Enter alias')

        self.fields['username'].widget.attrs['class'] = 'span9'
        self.fields['username'].widget.attrs['placeholder'] = _('Enter username')

        self.fields['email'].widget.attrs['class'] = 'span9'
        self.fields['email'].widget.attrs['placeholder'] = _('Enter email')

    password1 = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'span9',
            'placeholder': _('Enter password'),
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(attrs={
            'class': 'span9',
            'placeholder': _('Enter password again'),
        }),
        strip=False,
        help_text=_('Enter the same password as before'))

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        auth_password_validators = password_validation.get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
        password_validation.validate_password(password1, self.instance, auth_password_validators)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch'
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['alias'].widget.attrs['class'] = 'span9'
        self.fields['alias'].widget.attrs['placeholder'] = _('Enter desire name')

        self.fields['username'].widget.attrs['class'] = 'span9'
        self.fields['username'].widget.attrs['placeholder'] = _('Enter username')

        self.fields['email'].widget.attrs['class'] = 'span9'
        self.fields['email'].widget.attrs['placeholder'] = _('Enter email')

    password = ReadOnlyPasswordHashField()

    def clean_password(self):
        return self.initial["password"]


class LevelAdminModelForm(AddChangeModelForm):

    fields_without_classes = ('color', )
    disabled_fields = ('slug', )

    class Meta:
        widgets = {
            'description': utils_widgets.AutosizedTextarea(),
        }


class ProfileAdminModelForm(AddChangeModelForm):

    fields_without_classes = ('gender', 'crafts')

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        form_field_crafts = self.fields['crafts']
        base_widget = form_field_crafts.widget
        base_widget.attrs.update({'class': 'form-control'})

        form_field_crafts.widget = utils_widgets.SplitInputsArrayWidget(
            widget=base_widget, size=form_field_crafts.max_length
        )

    class Meta:
        widgets = {
            'about': utils_widgets.CKEditorWidget(),
            'signature': utils_widgets.TinyMCEWidget(),
            'date_birthday': utils_widgets.DateTimeWidget(),
            'gender': utils_widgets.HorizontalRadioSelect(),
        }
