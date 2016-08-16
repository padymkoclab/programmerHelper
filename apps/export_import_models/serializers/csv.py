"""
Serialize data to/from JSON
"""

import itertools
import json
import datetime
import decimal
import csv
import io
import sys
import uuid

from django.conf import settings
from django.apps import apps
from django.core.serializers.base import DeserializationError, DeserializedObject, build_instance
from django.core.serializers.python import (
    Deserializer as PythonDeserializer,
    Serializer as PythonSerializer,
    _get_model,
)
from django.db import DEFAULT_DB_ALIAS, models
from django.utils import six
from django.utils.timezone import is_aware
from django.utils.encoding import is_protected_type, force_text


class Serializer(PythonSerializer):
    """
    Convert a queryset to CSV.
    """

    def serialize(self, queryset, **options):
        """A method itself serialization. Added a some process until start the serialization."""

        # determinate fields for a CSV file
        fields = options.get('fields', None)
        self.set_fields(queryset[0], fields)

        # call serialization
        return super(Serializer, self).serialize(queryset, **options)

    def start_serialization(self):
        """A method calling on start a serialization."""

        # a list of headers for CSV with required fields: model and pk
        headers = ['model', 'pk'] + self.fieldnames
        self.writer = csv.DictWriter(self.stream, headers, delimiter=',', quoting=csv.QUOTE_ALL, quotechar='"')
        self.writer.writeheader()

    def start_object(self, obj):
        """A method calling on start a serialization of object."""

        # create a dict with initial data for required fields
        self._current = {
            'model': force_text(obj._meta),
            'pk': obj.pk,
        }

    def end_object(self, obj):
        """A method calling on finish a serialization of object."""

        # covert build-in Python`s types
        for k, v in self._current.items():
            if v is None:
                self._current[k] = 'NONE'
            elif v is True:
                self._current[k] = 'TRUE'
            elif v is False:
                self._current[k] = 'FALSE'

        # write row
        self.writer.writerow(self._current)

        # reser variable for new row
        self._current = None

    def set_fields(self, obj, fields):
        """Method determinating fields for a CSV file"""

        # get a model
        model = obj._meta.concrete_model

        # get simpe, fk and m2m fields
        local_fields = model._meta.local_fields
        many_to_many_fields = model._meta.many_to_many

        # reject fields created thought an intermediate model,
        # since objects must be created in that model, but not this# determinate fields for a CSV file
        many_to_many_fields = filter(lambda field: field.remote_field.through._meta.auto_created, many_to_many_fields)

        # determinate all serialized names of fields
        fieldnames = [field.name for field in itertools.chain(local_fields, many_to_many_fields) if field.serialize]

        # if a listing fields is passed, select only needed the fields
        if fields is not None:
            fieldnames = [fieldname for fieldname in fieldnames if fieldname in fields]

        # set variable on instance
        self.fieldnames = fieldnames

    def getvalue(self):

        # Grand-parent super
        return super(PythonSerializer, self).getvalue()


def Deserializer(object_list, **options):
    """
    Deserialize simple Python objects back into Django ORM instances.

    It's expected that you pass the Python objects themselves (instead of a
    stream or a string) to the constructor
    """

    db = options.pop('using', DEFAULT_DB_ALIAS)
    ignore = options.pop('ignorenonexistent', False)

    # first row in CSV files must be names of fields
    fieldnames, records = object_list.strip().partition('\r\n')[::2]

    # get list fields
    fieldnames = fieldnames.strip().split(',')

    # remove escape characters "" around a word
    fieldnames = [fieldname[1:-1] for fieldname in fieldnames]

    # create a in-memory file and write in it all the records
    # as well as made seek on begin of the file
    f = io.StringIO()
    f.write(records)
    f.seek(0)

    # create temprorary CSV DictReader from the previously created file
    # and determined fieldnames
    reader = csv.DictReader(f, fieldnames=fieldnames)

    # made iterations on rows in the reader
    for obj in reader:

        # try get model
        try:
            Model = _get_model(obj['model'])
        except DeserializationError:
            if ignore:
                continue
            else:
                raise

        # a variable for all deserialized data
        data = {}

        # get an object by pk
        if 'pk' in obj:
            try:
                data[Model._meta.pk.attname] = Model._meta.pk.to_python(obj['pk'])
            except Exception as e:
                raise DeserializationError.WithData(e, obj['model'], obj.get('pk'), None)

        # a variable for all deserialized data on manytomany fields
        m2m_data = {}

        # set of names all the model`s fields
        field_names = {f.name for f in Model._meta.get_fields()}

        # a dict with purely keys and values of real fields,
        # for it removed keys 'model' and 'pk',
        # besides 'pk' keep for save in ouput for an each instance
        purely_fields_and_values = obj.copy()
        purely_fields_and_values.pop('model')
        data['pk'] = purely_fields_and_values.pop('pk')

        # Handle each field
        for field_name, field_value in purely_fields_and_values.items():

            if ignore and field_name not in field_names:
                # skip fields no longer on model
                continue

            if isinstance(field_value, str):
                field_value = force_text(
                    field_value, options.get("encoding", settings.DEFAULT_CHARSET), strings_only=True
                )

            # convert from CSV to Python`s types
            if field_value == 'NONE':
                field_value = None
            elif field_value == 'TRUE':
                field_value = True
            elif field_value == 'FALSE':
                field_value = False

            field = Model._meta.get_field(field_name)

            # Handle M2M relations
            if field.remote_field and isinstance(field.remote_field, models.ManyToManyRel):
                model = field.remote_field.model

                # values of m2m field is keeping in string '[]'
                # so need convert it the string to a Python`s list

                # remove brackets '[' and ']' from value
                field_value = field_value[1:-1]

                # if value contains something, split tha to list
                # otherwise, convert to an empty list
                if field_value:
                    field_value = field_value.split(', ')
                else:
                    field_value = list()

                if hasattr(model._default_manager, 'get_by_natural_key'):
                    def m2m_convert(value):
                        if hasattr(value, '__iter__') and not isinstance(value, six.text_type):
                            return model._default_manager.db_manager(db).get_by_natural_key(*value).pk
                        else:
                            return force_text(model._meta.pk.to_python(value), strings_only=True)
                else:
                    m2m_convert = lambda v: force_text(model._meta.pk.to_python(v), strings_only=True)

                try:
                    m2m_data[field.name] = []
                    for pk in field_value:
                        m2m_data[field.name].append(m2m_convert(pk))
                except Exception as e:
                    raise DeserializationError.WithData(e, obj['model'], obj.get('pk'), pk)

            # Handle FK fields
            elif field.remote_field and isinstance(field.remote_field, models.ManyToOneRel):
                model = field.remote_field.model
                if field_value is not None:
                    try:
                        default_manager = model._default_manager
                        field_name = field.remote_field.field_name
                        if hasattr(default_manager, 'get_by_natural_key'):
                            if hasattr(field_value, '__iter__') and not isinstance(field_value, six.text_type):
                                obj = default_manager.db_manager(db).get_by_natural_key(*field_value)
                                value = getattr(obj, field.remote_field.field_name)
                                # If this is a natural foreign key to an object that
                                # has a FK/O2O as the foreign key, use the FK value
                                if model._meta.pk.remote_field:
                                    value = value.pk
                            else:
                                value = model._meta.get_field(field_name).to_python(field_value)
                            data[field.attname] = value
                        else:
                            data[field.attname] = model._meta.get_field(field_name).to_python(field_value)
                    except Exception as e:
                        raise DeserializationError.WithData(e, obj['model'], obj.get('pk'), field_value)
                else:
                    data[field.attname] = None

            # Handle all other fields
            else:
                try:
                    data[field.name] = field.to_python(field_value)
                except Exception as e:
                    raise DeserializationError.WithData(e, obj['model'], obj.get('pk'), field_value)

        obj = build_instance(Model, data, db)
        yield DeserializedObject(obj, m2m_data)
