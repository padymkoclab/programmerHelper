
import statistics

from django.db import models
from django.contrib.contenttypes.models import ContentType

from apps.core.utils import (
    get_statistics_count_objects_for_the_past_year,
    get_chart_count_objects_for_the_past_year,
)


class FlavourManager(models.Manager):
    """
    Manager for other models
    """

    def get_count_flavours(self):
        """ """

        return self.filter(flavours__isnull=False).values('flavours').count()

    def get_avg_count_flavours(self):
        """ """

        count_flavours = self.get_count_flavours()
        count_objects = self.count()

        return statistics.mean()


    def get_statistics_count_flavours_for_the_past_year(self):
        """ """

        ct_model_pk = ContentType.objects.get_for_model(self.model).pk
        model_field = self.model._meta.get_field('flavours')
        flavours = model_field.related_model._default_manager

        flavours_for_objects = flavours.filter(content_type_id=ct_model_pk)

        return get_statistics_count_objects_for_the_past_year(flavours_for_objects, 'date_added')

    def get_chart_count_flavours_for_the_past_year(self):
        """ """

        return get_chart_count_objects_for_the_past_year(
            self.get_statistics_count_flavours_for_the_past_year()
        )
