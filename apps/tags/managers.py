
import random
import collections

from django.utils.text import force_text
from django.db import models

import pygal

from utils.python.constants import PRETTY_COLORS
from utils.django.functions_db import Round

from .querysets import TagQuerySet


class TagManager(models.Manager):
    """
    Manager of a tags for other object had the tags.
    Important towards other model have field 'tags'.
    """

    def get_count_used_tags(self):
        """ """

        return self.values('tags').count()

    def get_count_distinct_used_tags(self):
        """ """

        return self.values('tags').distinct().count()

    def get_avg_count_tags(self):
        """ """

        self = self.objects_with_count_tags()
        return self.aggregate(avg=Round(
            models.functions.Coalesce(models.Avg('count_tags'), 0)
        ))['avg']

    def get_related_objects(self, obj):
        """Return objects the same type, with common tags in a decsent order by a level similarity, as next:
        object: count_common_tags."""

        # look for an objects with a same tags, considering an each tag
        related_objects_by_tags = list()
        for tag in obj.tags.iterator():
            related_objects_by_tag = self.exclude(pk=obj.pk).filter(tags=tag)
            related_objects_by_tags.extend(related_objects_by_tag)

        # count an objects by count a common tags and to return their in a descent order
        related_objects_by_tags_with_count_common_tags = collections.Counter(related_objects_by_tags).most_common()

        # got only a primary keys of related objects
        pk_used_tags = tuple(obj.pk for obj, count_common_tags in related_objects_by_tags_with_count_common_tags)

        # make filter in a queryset only the related objects
        only_objects_with_common_tags = self.filter(pk__in=pk_used_tags)

        # return the related objects as queryset in a descent order
        sql_for_ordering_objects = models.Case(*[models.When(pk=pk, then=i) for i, pk in enumerate(pk_used_tags)])
        related_objects = only_objects_with_common_tags.order_by(sql_for_ordering_objects)

        return related_objects

    def get_statistics_used_tags(self):
        """Return count a used tags on deternimed type objects."""

        used_tags = list()
        for obj in self.iterator():
            used_tags.extend(obj.tags.all())
        #
        counter_used_tags = collections.Counter(used_tags).most_common()

        return counter_used_tags

    def get_chart_most_used_tags(self):
        """ """

        config = pygal.Config(
            width=1070,
            explicit_size=True,
            margin_left=200,
            truncate_legend=30,
        )

        chart = pygal.Pie(config)

        stat = self.get_statistics_used_tags()[:50]

        for tag, count in stat:
            chart.add(force_text(tag), count)

        return chart.render()

    def get_most_common_tags(self, min_count=None):
        """ """

        raise NotImplementedError

    def display_cloud_tags(self, min_count=None):
        """ """

        raise NotImplementedError


TagManager = TagManager.from_queryset(TagQuerySet)


class PurelyTagManager(models.Manager):
    """
    Manager of a tags destined purely for tags.
    """

    def get_statistics_total_used_tags_by_type_objects(self):
        """ """

        related_fields_names = self.model._get_related_fields_names()

        stat = dict.fromkeys(related_fields_names, 0)

        for obj in self.prefetch_related():
            for related_field_name in related_fields_names:
                stat[related_field_name] += getattr(obj, related_field_name).count()

        stat2 = list()
        for related_field_name, count in stat.items():
            related_model = self.model._meta.get_field(related_field_name).related_model
            verbose_name_plural = related_model._meta.verbose_name_plural

            stat2.append((verbose_name_plural, count))

        return stat2

    def get_chart_total_used_tags_by_type_objects(self):
        """ """

        config = pygal.Config(
            width=800,
            height=500,
            explicit_size=True,
            legend_at_bottom=True,
            show_legend=True,
            half_pie=True,
        )

        chart = pygal.Pie(config)

        for label, count in self.get_statistics_total_used_tags_by_type_objects():
            chart.add(force_text(label), count)

        return chart.render()

    def display_cloud_tags(self, min_count=None, ordered=False, colored=True):
        """ """

        self = self.tags_with_total_count_usage().values('name', 'total_count_usage')

        def wrap_(obj):
            total_count_usage = obj['total_count_usage']
            if total_count_usage == 1:
                size = 1
            elif total_count_usage == 0:
                return ''
            else:
                size = total_count_usage / 100 + 1
            color = random.choice(PRETTY_COLORS)
            css_styles = 'font-size: {}em;color: {};'.format(size, color)
            return '<span style="{}">{}</span>&nbsp;'.format(css_styles, obj['name'])

        return ''.join(map(wrap_, self))
