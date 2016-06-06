
from django.db.models.functions import Func


class Round(Func):
    """

    """

    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 4)'
