
from django.db import connection


class ClassmethodProperty(property):
    """Realization merge two descriptors: @classmethod and @property (getter)

    A base taken from http://stackoverflow.com/questions/128573/using-property-on-classmethods
    """

    def __get__(self, obj, objtype):
        return self.fget.__get__(None, objtype)()


def count_queries(func):
    def wrap(*args, **kwargs):
        count_before = len(connection.queries)
        response = func(*args, **kwargs)
        count_after = len(connection.queries)
        print(count_after - count_before)
        return response
    return wrap
