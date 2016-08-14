"""
Serialize data to/from JSON
"""

import json
import datetime
import decimal
import csv
import sys
import uuid

from django.core.serializers.base import DeserializationError
from django.core.serializers.python import (
    Deserializer as PythonDeserializer, Serializer as PythonSerializer,
)
from django.utils import six
from django.utils.timezone import is_aware
from django.utils.encoding import is_protected_type


class Serializer(PythonSerializer):
    """
    Convert a queryset to CSV.
    """

    def serialize(self, queryset, **options):

        self.csv_kwargs = options.copy()
        self.queryset = queryset

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
        model = self.queryset.model._meta.concrete_model
        fields = model._meta.concrete_fields
        list_fields = [field for field in fields]
        self.obj_fields = [field.name for field in list_fields]

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
            self._current[field.name] = '${0}$'.format(value)
        else:
            self._current[field.name] = '%{0}%'.format(field.value_to_string(obj))

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


def Deserializer(stream_or_string, **options):
    """
    Deserialize a stream or string of JSON data.
    """
    if not isinstance(stream_or_string, (bytes, six.string_types)):
        stream_or_string = stream_or_string.read()
    if isinstance(stream_or_string, bytes):
        stream_or_string = stream_or_string.decode('utf-8')
    try:
        objects = json.loads(stream_or_string)
        for obj in PythonDeserializer(objects, **options):
            yield obj
    except GeneratorExit:
        raise
    except Exception as e:
        # Map to deserializer error
        six.reraise(DeserializationError, DeserializationError(e), sys.exc_info()[2])


class DjangoJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time, decimal types and UUIDs.
    """

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, decimal.Decimal):
            return str(o)
        elif isinstance(o, uuid.UUID):
            return str(o)
        else:
            return super(DjangoJSONEncoder, self).default(o)

# Older, deprecated class name (for backwards compatibility purposes).
DateTimeAwareJSONEncoder = DjangoJSONEncoder
