
from django.db import models


class DeterminateRating(models.Func):
    """
    Annotation for determinate rationg
    """

    function = None
    template = None

    raise NotImplementedError
