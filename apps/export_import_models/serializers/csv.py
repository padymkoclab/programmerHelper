"""
Serialize data to/from JSON
"""

import itertools
import json
import datetime
import decimal
import csv
import sys
import uuid

from django.core.serializers.base import DeserializationError
from django.core.serializers.python import (
    Deserializer as PythonDeserializer,
    Serializer as PythonSerializer,
)
from django.db import DEFAULT_DB_ALIAS, models
from django.utils import six
from django.utils.timezone import is_aware
from django.utils.encoding import is_protected_type


class Serializer(PythonSerializer):
    """
    Convert a queryset to CSV.
    """

    def serialize(self, queryset, **options):

        self.csv_kwargs = options.copy()
        self.first_instance = queryset[0]

        self.set_obj_fields()
        self.set_all_fields()

        # self.csv_kwargs.pop('fields', self.obj_fields)
        # self.csv_kwargs.pop('delimiter', ',')
        # self.csv_kwargs.pop('quoting', csv.QUOTE_ALL)
        # self.csv_kwargs.pop('quotechar', '"')

        return super(Serializer, self).serialize(queryset, **options)

    def start_serialization(self):
        self.writer = csv.DictWriter(self.stream, self.all_fields, delimiter=',', quoting=csv.QUOTE_ALL, quotechar='"')
        self.writer.writeheader()

    def start_object(self, obj):
        self._current = {'model': obj._meta.app_config.name}

    def end_object(self, obj):

        # self._current has the field data

        self.writer.writerow(self._current)
        self._current = None

    def set_obj_fields(self):

        #
        model = self.first_instance._meta.concrete_model

        #
        local_fields = model._meta.local_fields
        many_to_many_fields = model._meta.many_to_many

        #
        self.obj_fields = [field.name for field in itertools.chain(local_fields, many_to_many_fields)]

    def set_all_fields(self):
        self.all_fields = ['model'] + self.obj_fields

    def get_row_object(self, obj):
        row = {'model': obj._meta.app_config.name}

        for field_name in self.obj_fields:
            row[field_name] = getattr(obj, field_name)

        return row

    def getvalue(self):
        # Grand-parent super
        return super(PythonSerializer, self).getvalue()

    def handle_field(self, obj, field):

        value = field.value_from_object(obj)

        # Protected types (i.e., primitives like None, numbers, dates,
        # and Decimals) are passed through as is. All other values are
        # converted to string first.
        if is_protected_type(value):
            self._current[field.name] = value
        else:
            self._current[field.name] = field.value_to_string(obj)

    # def handle_fk_field(self, obj, field):
    #     if self.use_natural_foreign_keys and hasattr(field.remote_field.model, 'natural_key'):
    #         related = getattr(obj, field.name)
    #         if related:
    #             value = related.natural_key()
    #         else:
    #             value = None
    #     else:
    #         value = getattr(obj, field.get_attname())
    #         if not is_protected_type(value):
    #             value = field.value_to_string(obj)
    #     self._current[field.name] = value

    # def handle_m2m_field(self, obj, field):
    #     if field.remote_field.through._meta.auto_created:
    #         if self.use_natural_foreign_keys and hasattr(field.remote_field.model, 'natural_key'):
    #             m2m_value = lambda value: value.natural_key()
    #         else:
    #             m2m_value = lambda value: force_text(value._get_pk_val(), strings_only=True)
    #         self._current[field.name] = [m2m_value(related)
    #                            for related in getattr(obj, field.name).iterator()]


def Deserializer(object_list, **options):
    """
    Deserialize simple Python objects back into Django ORM instances.

    It's expected that you pass the Python objects themselves (instead of a
    stream or a string) to the constructor
    """

    db = options.pop('using', DEFAULT_DB_ALIAS)
    ignore = options.pop('ignorenonexistent', False)
