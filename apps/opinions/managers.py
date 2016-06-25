
from django.db import models


class OpinionManager(models.Manager):
    """Manager for working with opinons on other models."""

    def get_avg_scope(self):
        """Get total scope by all a scopes of objects."""

        self = self.model.objects.objects_with_scopes()
        dict_with_avg_scope = self.aggregate(avg_scope=models.Avg('scope'))
        return dict_with_avg_scope['avg_scope']

    def get_min_scope(self):
        """Get total scope by all a scopes of objects."""

        self = self.model.objects.objects_with_scopes()
        dict_with_avg_scope = self.aggregate(avg_scope=models.Min('scope'))
        return dict_with_avg_scope['avg_scope']

    def get_max_scope(self):
        """Get total scope by all a scopes of objects."""

        self = self.model.objects.objects_with_scopes()
        dict_with_avg_scope = self.aggregate(avg_scope=models.Max('scope'))
        return dict_with_avg_scope['avg_scope']
