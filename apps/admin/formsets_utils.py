
import uuid
import datetime

from django.db import models
from django.utils.html import format_html

from utils.django.datetime_utils import convert_date_to_django_date_format

from .utils import pretty_label_or_short_description


class InlineFormset(object):

    def __init__(self, inline, formset, request):
        self.formset = formset
        self.inline = inline
        self.request = request

        self.management_form = self.formset.management_form
        self.total_error_count = self.formset.total_error_count
        self.can_delete = self.formset.can_delete
        self.empty_form = self.formset.empty_form
        self.prefix = self.formset.prefix

        self.id = uuid.uuid1()

    def __iter__(self):
        for form in self.formset:

            instance = form.instance
            fields = self.inline.get_fields(self.request, instance)
            readonly_fields = self.inline.get_readonly_fields(self.request, instance)

            yield InlineFormsetForm(
                self.inline,
                form,
                fields,
                readonly_fields,
            )

    @property
    def fieldnames(self):
        editable_fields = self.inline.get_fields(self.request)
        readonly_fields = self.inline.get_readonly_fields(self.request)
        raw_fieldnames = editable_fields + tuple(field for field in readonly_fields if field not in editable_fields)

        fieldnames = list()
        model = self.inline.model
        for fieldname in raw_fieldnames:

            # field or method of a instance or method admin inline model
            field = getattr(model, fieldname, None)

            if callable(field):
                label = pretty_label_or_short_description(field)
            elif hasattr(field, 'field_name'):
                label = model._meta.get_field(fieldname).verbose_name
            else:
                method = getattr(self.inline, fieldname)
                label = pretty_label_or_short_description(method)

            fieldnames.append(label)

        return fieldnames


class InlineFormsetForm(object):

    def __init__(self, inline, form, fields, readonly_fields):
        self.inline = inline
        self.form = form
        self.fields = fields
        self.readonly_fields = readonly_fields

        self.all_fields = list(self.fields) + [field.name for field in self.form.hidden_fields()]

        self.instance = self.form.instance
        self.non_field_errors = self.form.non_field_errors
        self.errors = self.form.errors
        self.is_valid = self.form.is_valid
        self.prefix = self.form.prefix

    def __iter__(self):

        for fieldname in self.all_fields:
            if fieldname in self.readonly_fields:
                yield InlineFormsetFormReadonlyField(fieldname, self.form.instance, self.inline)
            else:
                yield InlineFormsetFormEditableField(fieldname, self.form)


class InlineFormsetFormEditableField(object):

    def __init__(self, fieldname, form):
        self.fieldname = fieldname
        self.form = form
        self.field = form[self.fieldname]
        self.is_readonly = False

        self.help_text = self.field.help_text
        self.id_for_label = self.field.id_for_label
        self.label = self.field.label
        self.errors = self.field.errors
        self.name = self.field.name
        self.is_hidden = self.field.is_hidden

    def __str__(self):
        return str(self.field)


class InlineFormsetFormReadonlyField(object):

    def __init__(self, fieldname, instance, inline_admin):
        self.fieldname = fieldname
        self.instance = instance
        self.inline_admin = inline_admin
        self.is_readonly = True

    @property
    def label(self):

        # field or method of a instance or method admin inline model
        field = getattr(self.instance, self.fieldname, None)

        model_fieldnames = [modelfield.name for modelfield in self.instance._meta.get_fields()]

        if callable(field):
            label = pretty_label_or_short_description(field)
        elif self.fieldname in model_fieldnames:
            label = self.instance._meta.get_field(self.fieldname).verbose_name
        else:
            method = getattr(self.inline_admin, self.fieldname)
            label = pretty_label_or_short_description(method)

        return label

    def get_value(self):

        # field or method of a instance or method admin inline model
        value = getattr(self.instance, self.fieldname, None)

        if callable(value):
            value = value()
        elif hasattr(self.inline_admin, self.fieldname):
            method = getattr(self.inline_admin, self.fieldname)
            value = method(self.instance)

        if isinstance(value, (datetime.datetime, datetime.date)):
            value = convert_date_to_django_date_format(value)

        if value is None:
            value = self.inline_admin.site_admin.empty_value_display

        return format_html('{}', value)

    def __str__(self):
        return self.get_value()
