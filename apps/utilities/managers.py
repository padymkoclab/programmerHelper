
# from django.utils.text import force_text
# from django.utils.safestring import mark_safe
from django.db import models

import pygal
from pygal.style import DefaultStyle
from pygal import Config

from utils.django.functions_db import Round


class CategoryManager(models.Manager):

    def get_avg_count_utilities_in_categories(self):
        """ """

        self = self.categories_with_count_utilities()
        avg = self.aggregate(avg=Round(models.Avg('count_utilities')))['avg']
        return avg or 0


class UtilityManager(models.Manager):

    def get_avg_count_opinions_in_utilities(self):
        """ """

        self = self.utilities_with_count_opinions()
        avg = self.aggregate(avg=Round(models.Avg('count_opinions')))['avg']
        return avg or 0

    def get_avg_count_comments_in_utilities(self):
        """ """

        self = self.utilities_with_count_comments()
        avg = self.aggregate(avg=Round(models.Avg('count_comments')))['avg']
        return avg or 0

    def get_count_opinions(self):
        """ """

        self = self.utilities_with_count_opinions()
        count_opinions = self.aggregate(sum=models.Sum('count_opinions'))['sum']
        return count_opinions or 0

    def get_count_comments(self):
        """ """

        self = self.utilities_with_count_comments()
        count_comments = self.aggregate(sum=models.Sum('count_comments'))['sum']
        return count_comments or 0

    def get_count_users_posted_comments(self):
        """ """

        return self.values('comments__user').distinct().count()

    def get_count_good_opinions(self):
        """ """

        return self.filter(opinions__is_useful=True).aggregate(count=models.Count('opinions'))['count']

    def get_count_bad_opinions(self):
        """ """

        return self.filter(opinions__is_useful=False).aggregate(count=models.Count('opinions'))['count']

    def get_most_popular_utilities(self):
        """ """

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

        if most_popular_utilities is None:
            config.width = 800

        chart = pygal.HorizontalBar(config)

        # add data to the chart and the conf
        if most_popular_utilities is not None:
            for i, utility in enumerate(most_popular_utilities):
                chart.add(str(i + 1), utility.mark)
        svg = chart.render()
        return svg

    def get_10_most_discussed_utilities(self):
        """ """

        raise NotImplementedError
