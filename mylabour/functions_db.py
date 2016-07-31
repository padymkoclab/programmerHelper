
from django.db import models
from django.db.models.functions import Func


class Round(Func):
    """

    """

    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 3)'


class ToStr(Func):
    """

    """

    function = 'CAST'
    template = '%(function)s(%(expressions)s AS TEXT)'


class ToChar(Func):
    """

    """

    function = 'CAST'
    template = '%(function)s(%(expressions)s AS VARCHAR)'


class Degrees(Func):
    """
    Returns numeric expression converted from radians to degrees.
    """

    function = 'DEGREES'


class Power(Func):
    """
    These two functions return the value of X raised to the power of Y.
    """

    function = 'POWER(X, Y)'


class Radians(Func):
    """
    This function returns the value of X, converted from degrees to radians.

    """

    function = 'RADIANS'


class Sqrt(Func):
    """
    This function returns the non-negative square root of X.
    """

    function = 'SQRT'


class Cast(Func):
    """
    Coerce an expression to a new field type.
    """
    function = 'CAST'
    template = '%(function)s(%(expressions)s AS %(db_type)s)'

    mysql_types = {
        models.fields.CharField: 'char',
        models.fields.IntegerField: 'signed integer',
        models.fields.FloatField: 'signed',
    }

    def __init__(self, expression, output_field):
        super(Cast, self).__init__(expression, output_field=output_field)

    def as_sql(self, compiler, connection, **extra_context):
        if 'db_type' not in extra_context:
            extra_context['db_type'] = self._output_field.db_type(connection)
        return super(Cast, self).as_sql(compiler, connection, **extra_context)

    def as_mysql(self, compiler, connection):
        extra_context = {}
        output_field_class = type(self._output_field)
        if output_field_class in self.mysql_types:
            extra_context['db_type'] = self.mysql_types[output_field_class]
        return self.as_sql(compiler, connection, **extra_context)

    def as_postgresql(self, compiler, connection):
        # CAST would be valid too, but the :: shortcut syntax is more readable.
        return self.as_sql(compiler, connection, template='%(expressions)s::%(db_type)s')
