
from django.contrib.contenttypes.models import ContentType
from django.db import models

import pygal

from utils.django.functions_db import Round
from utils.django.models_utils import get_statistics_count_objects_for_the_past_year as get_statistics

from .querysets import OpinionQuerySet


class OpinionManager(models.Manager):
    """Manager for working with opinons on other models."""

    def get_count_opinions(self):
        """ """

        return self.objects_with_count_opinions().aggregate(
            result=models.functions.Coalesce(
                models.Sum('count_opinions'), 0
            )
        )['result']

    def get_avg_count_opinions(self):
        """ """

        return self.objects_with_count_opinions().aggregate(
            result=Round(
                models.functions.Coalesce(
                    models.Avg('count_opinions'), 0
                )
            )
        )['result']

    def get_count_critics(self):
        """ """

        return self.aggregate(result=models.Count(
            models.Case(
                models.When(opinions__is_useful=False, then=1),
                output_field=models.IntegerField()
            )
        ))['result']

    def get_count_supporters(self):
        """ """

        return self.aggregate(result=models.Count(
            models.Case(
                models.When(opinions__is_useful=True, then=1),
                output_field=models.IntegerField()
            )
        ))['result']

    def get_statistics_count_opinions_for_the_past_year(self):
        """ """

        ct_model_pk = ContentType.objects.get_for_model(self.model).pk
        model_field = self.model._meta.get_field('opinions')
        all_opinions = model_field.related_model._default_manager

        opinions_for_objects = all_opinions.filter(content_type_id=ct_model_pk)
        critic_opinions_for_objects = opinions_for_objects.filter(is_useful=False)
        supporters_opinions_for_objects = opinions_for_objects.filter(is_useful=True)

        statistics_for_all_opinions_for_objects = \
            get_statistics(opinions_for_objects, 'date_added')

        dates, count_opinions_by_the_past_year = zip(*statistics_for_all_opinions_for_objects)

        statistics_for_critic_opinions_for_objects = \
            get_statistics(critic_opinions_for_objects, 'date_added')
        statistics_for_supporters_opinions_for_objects = \
            get_statistics(supporters_opinions_for_objects, 'date_added')

        count_critic_opinions_for_objects_by_the_past_year = \
            tuple(zip(*statistics_for_critic_opinions_for_objects))[1]
        count_supporters_opinions_for_objects_by_the_past_year = \
            tuple(zip(*statistics_for_supporters_opinions_for_objects))[1]

        statistics = zip(
            dates,
            count_opinions_by_the_past_year,
            count_critic_opinions_for_objects_by_the_past_year,
            count_supporters_opinions_for_objects_by_the_past_year,
        )
        return tuple(statistics)

    def get_chart_count_opinions_for_the_past_year(self):
        """ """

        config = pygal.Config()
        config.width = 800
        config.height = 500
        config.explicit_size = True
        config.fill = True
        config.show_legend = True
        config.legend_at_bottom = True
        config.legend_at_bottom_columns = 1
        config.interpolate = 'hermite'
        config.interpolation_parameters = {'type': 'cardinal', 'c': .75}

        chart = pygal.Bar(config)

        statistics = self.get_statistics_count_opinions_for_the_past_year()

        dates, *data = zip(*statistics)

        list_total_count_opinions, list_count_critical_opinions, list_count_supporting_opinions = data

        chart.x_labels = dates
        chart.add('Total count opinions', list_total_count_opinions)
        chart.add('Count critical opinions', list_count_critical_opinions)
        chart.add('Count supporting opinions', list_count_supporting_opinions)
        svg = chart.render()
        return svg


OpinionManager = OpinionManager.from_queryset(OpinionQuerySet)
