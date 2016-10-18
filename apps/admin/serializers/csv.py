
import csv

from django.conf import settings
from django.utils.text import force_text
from django.apps import apps
from django.db import DEFAULT_DB_ALIAS
from django.core.serializers import base as base_serializer


class Serializer(base_serializer.Serializer):
    """

    """

    def serialize(self, queryset, **options):

        self.model_meta = queryset.model._meta

        super().serialize(queryset, **options)

    def start_serialization(self):

        self.fieldnames = [field.name for field in self.model_meta.concrete_fields if field != self.model_meta.pk]
        self.fieldnames.insert(0, 'model')
        self.fieldnames.insert(1, 'pk')

        self.writer = csv.DictWriter(self.stream, self.fieldnames)
        self.writer.writeheader()

    def end_serialization(self):
        pass

    def start_object(self, obj):

        self.data = dict(
            model=self.model_meta.label,
            pk=obj.pk,
        )

    def end_object(self, obj):

        self.writer.writerow(self.data)

    def handle_field(self, obj, field):

        fieldname = field.name
        self.data[fieldname] = getattr(obj, fieldname)

    def handle_fk_field(self, obj, field):

        raise NotImplementedError('subclasses of Serializer must provide an handle_fk_field() method')

    def handle_m2m_field(self, obj, field):

        raise NotImplementedError('subclasses of Serializer must provide an handle_m2m_field() method')

    def getvalue(self):

        if callable(getattr(self.stream, 'getvalue', None)):
            return self.stream.getvalue()
        self.stream.close()


class Deserializer(base_serializer.Deserializer):

    def __init__(self, stream_or_string, **kwargs):

        self.kwargs = kwargs

        self.db = self.kwargs.pop('using', DEFAULT_DB_ALIAS)
        self.ignore = self.kwargs.pop('ignorenonexistent', False)

        self.stream = stream_or_string
        if isinstance(stream_or_string, bytes):
            self.stream = self.stream.decode(settings.DEFAULT_CHARSET)

        self.reader = self.get_reader()

        self.only_fieldnames = self.reader.fieldnames[:]
        self.only_fieldnames.remove('model')
        self.only_fieldnames.remove('pk')

    def __next__(self):

        row = next(self.reader)
        return self.handle_row(row)

        raise StopIteration

    def get_reader(self):

        rows = self.stream.split('\n')

        return csv.DictReader(rows)

    def handle_row(self, row):

        model_name = row.get('model')

        try:
            model = apps.get_model(model_name)
        except (KeyError, LookupError):
            if not self.ignore:
                raise base_serializer.DeserializationError(
                    "Invalid model identifier: '{}'".format(model_name)
                )

        data = {}

        pk = row.get('pk')
        try:
            data[model._meta.pk.attname] = model._meta.pk.to_python(pk)
        except Exception as e:
            raise base_serializer.DeserializationError.WithData(
                e, model_name, pk, None,
            )

        real_fieldnames = [field.name for field in model._meta.get_fields()]

        for column_name in self.only_fieldnames:
            if column_name not in real_fieldnames and self.ignore:
                continue

            m2m_data = {}

            value = row[column_name]

            value = force_text(value, settings.DEFAULT_CHARSET, strings_only=True)

            field = model._meta.get_field(column_name)

            try:
                data[field.name] = field.to_python(value)
            except Exception as e:
                raise base_serializer.DeserializationError.WithData(
                    e, model, pk, value
                )
            data

        obj = base_serializer.build_instance(model, data, self.db)
        return base_serializer.DeserializedObject(obj, m2m_data)
