
import datetime

from django.forms.utils import ErrorList
from django.db.models.query_utils import DeferredAttribute
from django.utils.html import format_html, format_html_join
from django.utils.text import force_text
from django.utils.safestring import SafeText

from utils.django.datetime_utils import convert_date_to_django_date_format

from .utils import pretty_label_or_short_description


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

    @property
    def total_error_count(self):
        return len(self.form.errors.values()) + len(self.form.non_field_errors())


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

        if value is None:
            return self.model_admin.site_admin.empty_value_display

        return str(value)


class BootstrapErrorList(ErrorList):

    def __str__(self):
        return self.as_ul()

    def as_ul(self):

        if not self.data:
            return ''

        return format_html(
            '<ol class="{}">{}</ol>',
            self.error_class,
            format_html_join(
                '',
                '<li class="text-danger">{}</li>',
                ((force_text(i), ) for i in self)
            )
        )


# class InlineFieldset()
