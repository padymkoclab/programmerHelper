
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from passwords.fields import PasswordField
from passwords.validators import (
    DictionaryValidator, LengthValidator, ComplexityValidator)

from .models import User


class Createuserform(forms.ModelForm):
    """
    Form for creating user
    """

    password = PasswordField(label=_('Passowrd'))
    field = forms.CharField(validators=[
        DictionaryValidator(words=['banned_word'], threshold=0.9),
        LengthValidator(min_length=8),
        ComplexityValidator(complexities=dict(
            UPPER=1,
            LOWER=1,
            DIGITS=1
        ),
        )])

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'date_birthday')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': _('Enter your email')}),
        }


# Admin forms

class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """

    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput,
        help_text=_('Enter the same password as before, for verification.'))

    class Meta:
        model = User
        fields = ('email', 'username', 'date_birthday')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
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

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email',)

    def clean_password(self):
        return self.initial["password"]
