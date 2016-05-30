
from django.db import models


class CourseQuerySet(models.QuerySet):
    """
    QuerySet for using with queryset model Course
    """

    def creators_courses(self):
        return self.values_list('authorship', flat=True).distinct()


class CourseManager(models.Manager):
    """
    Model manager for model Couse
    """
    pass
