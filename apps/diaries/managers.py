
from django.db import models

from .querysets import DiaryQuerySet, PartitionQuerySet


class DiaryManager(models.Manager):
    """ """

    pass


DiaryManager = DiaryManager.from_queryset(DiaryQuerySet)


class PartitionManager(models.Manager):

    pass


PartitionManager = PartitionManager.from_queryset(PartitionQuerySet)
