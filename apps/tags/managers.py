
import collections

from django.db import models


class TagManager(models.Manager):
    """
    Manager of a tags for other object had the tags.
    Important towards other model have field 'tags'.
    """

    def get_related_objects_by_tags(self, obj):
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

    def get_statistics_by_count_used_tags(self):
        """Return count a used tags on deternimed type objects."""

        used_tags = list()
        for obj in self.iterator():
            used_tags.extend(obj.tags.all())
        #
        counter_used_tags = collections.Counter(used_tags).most_common()

        return counter_used_tags


class PurelyTagManager(models.Manager):
    """
    Manager of a tags destined purely for tags.
    """

    def remove_less_used_tags(self):
        """Remove a less-used tags."""

        raise NotImplementedError

    def get_statistics_total_used_tags(self):
        raise NotImplementedError
