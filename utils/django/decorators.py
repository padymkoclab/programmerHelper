
from django.db import connection


def count_queries(func):
    def wrap(*args, **kwargs):
        count_before = len(connection.queries)
        response = func(*args, **kwargs)
        count_after = len(connection.queries)
        print(count_after - count_before)
        return response
    return wrap
