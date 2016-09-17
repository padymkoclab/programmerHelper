
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.core.utils import (
    get_statistics_count_objects_for_the_past_year,
    get_chart_count_objects_for_the_past_year,
)

from .querysets import ReplyQuerySet
from .models import Reply


class ReplyManager(models.Manager):
    """

    """

    def check(self, **kwargs):

        response = super().check(**kwargs)

        # not possible make access to content models in __init__() or contribute_to_class()
        # but here it is worked

        # access to a ContentTypeModel of an attached manager
        self.ContentTypeModel = ContentType.objects.get_for_model(self.model)

        # a queryset of replies for that objects
        self.queryset = Reply.objects.filter(content_type=self.ContentTypeModel)

        return response

    def get_count_replies(self):
        """ """

        return self.queryset.count()

    def get_avg_count_replies(self):
        """ """

        if self.exists():
            avg = self.queryset.count() / self.count()
            return round(avg, 3)

        return .0

    def get_statistics_count_replies_for_the_past_year(self):
        """ """

        return get_statistics_count_objects_for_the_past_year(self.queryset, 'date_added')

    def get_chart_count_replies_for_the_past_year(self):
        """ """

        return get_chart_count_objects_for_the_past_year(
            self.get_statistics_count_replies_for_the_past_year()
        )


ReplyManager = ReplyManager.from_queryset(ReplyQuerySet)
