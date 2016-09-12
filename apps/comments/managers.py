
from django.contrib.contenttypes.models import ContentType
from utils.django.functions_db import Round
from django.db import models

import pygal

from utils.django.models_utils import get_statistics_count_objects_for_the_past_year as get_statistics

from .querysets import CommentQuerySet


class CommentManager(models.Manager):
    """ """

    def get_avg_count_comments(self):
        """ """

        return self.objects_with_count_comments().aggregate(
            result=Round(
                models.functions.Coalesce(
                    models.Avg('count_comments'), 0
                )
            )
        )['result']

    def get_count_comments(self):
        """ """

        return self.objects_with_count_comments().aggregate(
            result=models.functions.Coalesce(
                models.Sum('count_comments'), 0
            )
        )['result']

    def get_count_distinct_users_posted_comments(self):
        """ """

        return self.values('comments__user').distinct().filter(comments__isnull=False).count()

    def get_statistics_count_comments_for_the_past_year(self):
        """ """

        ct_model_pk = ContentType.objects.get_for_model(self.model).pk
        model_field = self.model._meta.get_field('comments')
        comments = model_field.related_model._default_manager

        comments_for_objects = comments.filter(content_type_id=ct_model_pk)

        return get_statistics(comments_for_objects, 'date_added')

    def get_chart_count_comments_for_the_past_year(self):
        """ """

        config = pygal.Config()
        config.width = 800
        config.height = 500
        config.explicit_size = True
        config.fill = True
        config.show_legend = False
        config.interpolate = 'hermite'
        config.interpolation_parameters = {'type': 'cardinal', 'c': .75}

        chart = pygal.StackedLine(config)

        statistics = self.get_statistics_count_comments_for_the_past_year()

        dates, data = zip(*statistics)

        chart.x_labels = dates
        chart.add('Count comments', data)
        svg = chart.render()
        return svg


CommentManager = CommentManager.from_queryset(CommentQuerySet)
