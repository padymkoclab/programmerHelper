
import datetime

from django.db.models.query_utils import DeferredAttribute
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe, SafeText

from utils.django.datetime_utils import convert_date_to_django_date_format

from .utils import pretty_label_or_short_description


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


class AddChangeModelForm(forms.ModelForm):

    fields_without_classes = tuple()
    disabled_fields = tuple()
    fields_placeholders = tuple()
    addons = dict()

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if self.fields_without_classes is not '__all__':

            for name, field in self.fields.items():

                if name in self.fields_without_classes:
                    continue

                classes = getattr(field.widget.attrs, 'class', [])
                classes.append('form-control')

                field.widget.attrs['class'] = ' '.join(classes)

                if name in self.disabled_fields:
                    field.disabled = True

                verbose_name = self.Meta.model._meta.get_field(name).verbose_name

                field.widget.attrs['placeholder'] = 'Enter {}'.format(verbose_name.lower())

                field.help_text = self._get_help_text_to_field(field)

    @staticmethod
    def _get_help_text_to_field(field):

        help_text = field.help_text + '<br />' if field.help_text else ''

        min_length = getattr(field, 'min_length', -1)
        max_length = getattr(field, 'max_length', -1)

        if (min_length == -1 and max_length == -1) or (min_length is None and max_length is None):
            length_help_text = ''
        # elif min_length is not None and max_length is None:
        #     length_help_text = 'Length from {} characters.'.format(min_length)
        elif min_length is None and max_length > 1:
            length_help_text = 'Length not more then {} characters.'.format(max_length)
        else:
            length_help_text = 'Length from {} to {} characters.'.format(min_length, max_length)

        help_text = mark_safe(help_text + length_help_text)

        return help_text


class AddChangeDisplayForm:

    def __init__(self, form, fieldsets, readonly_fields, model_admin):
        self.fieldsets = fieldsets
        self.form = form
        self.readonly_fields = readonly_fields
        self.model_admin = model_admin

    def __iter__(self):

        for name, options in self.fieldsets:
            yield FieldSet(self.form, name, self.readonly_fields, self.model_admin, **options)


class FieldSet:

    def __init__(self, form, name, readonly_fields, model_admin, fields, classes=None, description=None):
        self.form = form
        self.name = name
        self.fields = fields
        self.readonly_fields = readonly_fields
        self.model_admin = model_admin

        self.classes = classes
        self.description = description

    def __iter__(self):
        for field_name in self.fields:
            yield FieldSetLine(self.form, field_name, self.readonly_fields, self.model_admin)


class FieldSetLine:

    def __init__(self, form, field_name, readonly_fields, model_admin):

        if field_name in form.fields and field_name not in readonly_fields:
            self.field = ActiveFormField(form, field_name, model_admin)
        else:
            self.field = ReadonlyField(form, field_name, model_admin)


class ActiveFormField:

    def __init__(self, form, field_name, model_admin):
        self.field = form[field_name]
        self.is_readonly = False
        self.model_admin = model_admin

    def label_tag(self):
        return self.field.label_tag(attrs={'class': 'col-xs-2 control-label'})

    def help_text(self):
        return self.field.help_text

    def errors(self):
        return self.field.errors

    def __str__(self):
        return format_html(self.field.as_widget())


class ReadonlyField:

    ATTR_ERROR_MSG = 'Intance or admin model class has not attribute "{}"'

    def __init__(self, form, field_name, model_admin):
        self.field_name = field_name
        self.form = form
        self.is_readonly = True
        self.model_admin = model_admin
        self.instance = self.form.instance

    def label_tag(self):
        return format_html(
            '<label class="col-xs-2 control-label">{}{}</label>',
            self.get_label(),
            self.form.label_suffix,
        )

    def help_text(self):
        if self.field_name in self.form.fields:
            return self.form[self.field_name].help_text
        return

    def errors(self):
        if self.field_name in self.form.fields:
            return self.form[self.field_name].errors
        return

    def __str__(self):
        return self.get_value()

    def get_label(self):

        # label of editable field
        if self.field_name in self.form.fields:
            return self.form[self.field_name].label

        # label of outside function or lambda-function
        elif callable(self.field_name):
            return pretty_label_or_short_description(self.field_name)

        # it is string definition of method a model or its admin class
        else:

            # method admin class
            model_admin_method = getattr(self.model_admin, self.field_name, None)
            if model_admin_method is not None:
                return pretty_label_or_short_description(model_admin_method)

            else:
                instance_method_or_field = getattr(self.model_admin.model, self.field_name, None)

                if instance_method_or_field is not None:

                    # method
                    if callable(instance_method_or_field):
                        return pretty_label_or_short_description(instance_method_or_field)

                    # property
                    elif isinstance(instance_method_or_field, property):
                        instance_method_or_field = instance_method_or_field.fget
                        return pretty_label_or_short_description(instance_method_or_field)

                    # a non editable field
                    elif isinstance(instance_method_or_field, DeferredAttribute):
                        return self.model_admin.model._meta.get_field(self.field_name).verbose_name

        # if not found to declared conditions raise an exception
        raise AttributeError(self.ATTR_ERROR_MSG.format(self.field_name))

    def get_raw_value(self):

        # if instance does not exists requert always empty value
        if self.instance is None:
            return self.model_admin.site_admin.empty_value_display

        # if instance exists, get value as initial in a hidden field
        # and display it as readonly in label
        if self.field_name in self.form.fields:
            field = self.form[self.field_name]
            rendered = field.as_hidden()
            initial = field.initial or self.model_admin.site_admin.empty_value_display
            return format_html('{}<span>{}</span>', rendered, initial)

        # value from an outside function or lambda
        elif callable(self.field_name):
            return self.field_name(self.instance)

        # value from model ot its admin class
        else:

            # method admin class
            model_admin_method = getattr(self.model_admin, self.field_name, None)
            if model_admin_method is not None:
                return model_admin_method(self.instance)

            # get value from instance
            else:
                instance_method_or_field = getattr(self.model_admin.model, self.field_name, None)

                if instance_method_or_field is not None:

                    # method
                    if callable(instance_method_or_field):
                        return getattr(self.instance, self.field_name)()

                    # property
                    elif isinstance(instance_method_or_field, property):
                        return getattr(self.instance, self.field_name)

                    # a non editable field
                    elif isinstance(instance_method_or_field, DeferredAttribute):
                        return getattr(self.instance, self.field_name)

        # if not found to declared conditions raise an exception
        raise AttributeError(self.ATTR_ERROR_MSG.format(self.field_name))

    def get_value(self):

        value = self.get_raw_value()

        if isinstance(value, SafeText):
            return value

        if isinstance(value, datetime.date):
            return convert_date_to_django_date_format(value)

        return str(value)
