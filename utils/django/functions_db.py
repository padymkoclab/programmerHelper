
from django.db import models
from django.db.models.expressions import Func


class IsNull(models.Func):
    """
    Used for made entries with value Null (Pythonic is None) as last in queryset
    """

    template = '%(expressions)s IS NULL'


class ArrayLength(models.Func):
    """Postgres specific function for annotation

    Usage for 1-dimension array:
        Stuff.objects.annotate(count_things=ArrayLength('things', *(1, )))

    """

    function = 'array_length'


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

# MOD
# PI
# POWER
# FLOOR
# CEIL
# GREATEST
# LEAST
