
# from django.utils.text import force_text
# from django.utils.safestring import mark_safe
from django.db import models

import pygal
from pygal.style import DefaultStyle
from pygal import Config

from mylabour.functions_db import Round


class UtilityCategoryManager(models.Manager):

    def get_avg_count_utilities_in_categories(self):

        return self.categories_with_count_utilities().aggregate(
            avg=Round(models.Avg('count_utilities'))
        )['avg']


class UtilityManager(models.Manager):

    def get_avg_count_opinions_in_utilities(self):

        return self.utilities_with_count_opinions().aggregate(
            avg=Round(models.Avg('count_opinions'))
        )['avg']

    def get_avg_count_comments_in_utilities(self):

        return self.utilities_with_count_comments().aggregate(
            avg=Round(models.Avg('count_comments'))
        )['avg']

    def get_count_opinions(self):

        return self.utilities_with_count_opinions().aggregate(sum=models.Sum('count_opinions'))['sum']

    def get_count_comments(self):

        return self.utilities_with_count_comments().aggregate(sum=models.Sum('count_comments'))['sum']

    def get_count_users_posted_comments(self):

        return self.values('comments__user').distinct().count()

    def get_count_good_opinions(self):

        return self.filter(opinions__is_useful=True).aggregate(count=models.Count('opinions'))['count']

    def get_count_bad_opinions(self):

        return self.filter(opinions__is_useful=False).aggregate(count=models.Count('opinions'))['count']

    def get_most_popular_utilities(self):

        utilities_with_marks = self.utilities_with_marks().filter(mark__isnull=False)
        if utilities_with_marks.exists():
            return utilities_with_marks.order_by('-mark')[:10]

    def get_chart_most_popular_utilities(self):

        # get objects
        most_popular_utilities = self.get_most_popular_utilities()

        # conf for a chart
        config = Config()
        config.interpolate = 'cubic'
        config.style = DefaultStyle
        config.show_legend = True
        config.legend_at_bottom = True
        config.legend_at_bottom_columns = 5
        config.fill = True
        config.width = 500
        config.height = 500
        config.explicit_size = True
        chart = pygal.HorizontalBar(config)

        # add data to the chart and the conf
        for i, utility in enumerate(most_popular_utilities):
            chart.add(str(i + 1), utility.mark)

        svg = chart.render()
        return svg

    def get_10_most_discussed_utilities(self):

        return
