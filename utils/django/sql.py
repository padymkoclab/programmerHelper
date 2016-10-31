
from django.db import models
from django.db import connections
from django.db.models.sql.compiler import SQLCompiler


class NullsLastCompiler(SQLCompiler):

    # source code https://github.com/django/django/blob/master/django/db/models/sql/compiler.py

    def get_order_by(self):

        result = super(NullsLastCompiler, self).get_order_by()

        # if result exists and backend is PostgreSQl
        if result and self.connection.vendor == 'postgresql':

            # modified raw SQL code to ending on NULLS LAST after ORDER BY
            # more info https://www.postgresql.org/docs/9.5/static/queries-order.html
            result = [
                (expression, (sql + ' NULLS LAST', params, is_ref))
                for expression, (sql, params, is_ref) in result
            ]

        return result


class NullsLastQuery(models.sql.Query):

    # source code https://github.com/django/django/blob/master/django/db/models/sql/query.py
    def get_compiler(self, using=None, connection=None):
        if using is None and connection is None:
            raise ValueError("Need either using or connection")
        if using:
            connection = connections[using]

        # return own compiler
        return NullsLastCompiler(self, connection, using)


class NullsLastQuerySet(models.QuerySet):

    # source code https://github.com/django/django/blob/master/django/db/models/query.py
    def __init__(self, model=None, query=None, using=None, hints=None):

        super(NullsLastQuerySet, self).__init__(model, query, using, hints)

        # replace on own Query
        self.query = query or NullsLastQuery(model)
