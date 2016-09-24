
from django.db import models

from .querysets import DiaryQuerySet


class DiaryManager(models.Manager):
    """ """

    pass


DiaryManager = DiaryManager.from_queryset(DiaryQuerySet)
