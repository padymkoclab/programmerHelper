
from django.contrib.contenttypes.models import ContentType
from django.db import models

import pygal

from utils.django.model_utils import get_statistics_count_objects_for_the_past_year as get_statistics
from utils.django.functions_db import Round


class SolutionManager(models.Manager):
    """
    Model manager for solutions.
    """

    def complain_on_the_solution(self, solution):
        """Complain on the solution sended admin and author corresponding notification."""

        raise NotImplementedError

    def get_avg_count_tags(self):
        """ """

        return self.solutions_with_count_tags().aggregate(
            result=Round(
                models.functions.Coalesce(
                    models.Avg('count_tags'), 0
                )
            )
        )['result']

    def get_count_usaged_tags(self):
        """ """

        return self.values('tags').count()

    def get_count_unique_usaged_tags(self):
        """ """

        return self.values('tags').distinct().count()

    def get_avg_count_comments(self):
        """ """

        return self.solutions_with_count_comments().aggregate(
            result=Round(
                models.functions.Coalesce(
                    models.Avg('count_comments'), 0
                )
            )
        )['result']

    def get_avg_count_opinions(self):
        """ """

        return self.solutions_with_count_opinions().aggregate(
            result=Round(
                models.functions.Coalesce(
                    models.Avg('count_opinions'), 0
                )
            )
        )['result']

    def get_count_opinions(self):
        """ """

        return self.solutions_with_count_opinions().aggregate(
            result=models.functions.Coalesce(
                models.Sum('count_opinions'), 0
            )
        )['result']

    def get_count_comments(self):
        """ """

        return self.solutions_with_count_comments().aggregate(
            result=models.functions.Coalesce(
                models.Sum('count_comments'), 0
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

    def get_statistics_count_comments_for_the_past_year(self):
        """ """

        ct_model_pk = ContentType.objects.get_for_model(self.model).pk
        model_field = self.model._meta.get_field('comments')
        comments = model_field.related_model._default_manager

        comments_for_solutions = comments.filter(content_type_id=ct_model_pk)

        return get_statistics(comments_for_solutions, 'date_added')

    def get_statistics_count_opinions_for_the_past_year(self):
        """ """

        ct_model_pk = ContentType.objects.get_for_model(self.model).pk
        model_field = self.model._meta.get_field('opinions')
        all_opinions = model_field.related_model._default_manager

        opinions_for_solutions = all_opinions.filter(content_type_id=ct_model_pk)
        critic_opinions_for_solutions = opinions_for_solutions.filter(is_useful=False)
        supporters_opinions_for_solutions = opinions_for_solutions.filter(is_useful=True)

        statistics_for_all_opinions_for_solutions = \
            get_statistics(opinions_for_solutions, 'date_added')

        dates, count_opinions_by_the_past_year = zip(*statistics_for_all_opinions_for_solutions)

        statistics_for_critic_opinions_for_solutions = \
            get_statistics(critic_opinions_for_solutions, 'date_added')
        statistics_for_supporters_opinions_for_solutions = \
            get_statistics(supporters_opinions_for_solutions, 'date_added')

        count_critic_opinions_for_solutions_by_the_past_year = \
            tuple(zip(*statistics_for_critic_opinions_for_solutions))[1]
        count_supporters_opinions_for_solutions_by_the_past_year = \
            tuple(zip(*statistics_for_supporters_opinions_for_solutions))[1]

        stat_data = zip(
            count_opinions_by_the_past_year,
            count_critic_opinions_for_solutions_by_the_past_year,
            count_supporters_opinions_for_solutions_by_the_past_year,
        )

        statistics = zip(dates, stat_data)
        return tuple(statistics)

    def get_statistics_count_solutions_for_the_past_year(self):
        """ """

        return get_statistics(self, 'date_added')

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

        dates, data = zip(*statistics)

        a, b, c = zip(*data)

        chart.x_labels = dates
        chart.add('Total count opinions', a)
        chart.add('Count critical opinions', b)
        chart.add('Count supporting opinions', c)
        svg = chart.render()
        return svg

    def get_chart_count_solutions_for_the_past_year(self):
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

        statistics = self.get_statistics_count_solutions_for_the_past_year()

        dates, data = zip(*statistics)

        chart.x_labels = dates
        chart.add('Count solutions', data)
        svg = chart.render()
        return svg
