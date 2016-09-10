
import collections

from django.db import models

import pygal

from utils.django.model_utils import get_statistics_count_objects_for_the_past_year as get_statistics


class SnippetManager(models.Manager):
    """
    Model manager for snippets.
    """

    def change_lexer_of_snippet(self, snippet, lexer):
        """Change lexer of snippet."""

        snippet.lexer = lexer
        snippet.full_clean()
        snippet.save()

    def make_snippet_as_pythonic(self, snippet):
        """Set lexer python for snippet."""

        self.change_lexer_of_snippet(snippet=snippet, lexer='python3')

    def get_statistics_usage_lexers(self):
        """Getting a statistics by total usage of each a lexer on all a snippets."""

        used_lexers = self.values_list('lexer', flat=True)

        count_used_lexers = collections.Counter(used_lexers).most_common()

        count_used_lexers.sort(key=lambda x: x[1], reverse=True)

        lexers_and_labels = dict(self.model._meta.get_field('lexer').choices)

        return [(lexers_and_labels[lexer], count)for lexer, count in count_used_lexers]

    def get_chart_statistics_usage_lexers(self):
        """Getting a statistics by total usage of each a lexer on all a snippets."""

        config = pygal.Config()

        config.width = 800
        # config.height = 500
        config.explicit_size = True
        config.legend_at_bottom = True
        config.legend_at_bottom_columns = 3
        config.show_legend = True
        config.style = pygal.style.DefaultStyle()

        chart = pygal.Pie(config)

        data = self.get_statistics_usage_lexers()

        for lexer, count_usage in data:
            chart.add(lexer, count_usage)

        svg = chart.render()
        return svg

    def get_statistics_count_snippets_for_the_past_year(self):
        """ """

        return get_statistics(self, 'date_added')

    def get_chart_count_snippets_for_the_past_year(self):
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

        statistics = self.get_statistics_count_snippets_for_the_past_year()

        dates, data = zip(*statistics)

        chart.x_labels = dates
        chart.add('Count snippets', data)
        svg = chart.render()
        return svg
