
import collections

from django.utils.translation import ugettext_lazy as _


class TagsModelMixin:

    def get_count_tags(self):
        """ """

        if hasattr(self, 'count_tags'):
            return self.count_tags

        return self.tags.count()
    get_count_tags.admin_order_field = 'count_tags'
    get_count_tags.short_description = _('Count tags')

    def get_related_objects(self):

        related_objects_by_tags = list()

        field_related_name = self._meta.get_field('tags').rel.related_name

        for tag in self.tags.all():

            related_name = getattr(tag, field_related_name)
            related_objects_by_tag = related_name.exclude(pk=self.pk)
            related_objects_by_tags.extend(related_objects_by_tag)

        counter_related_objects_by_tags = collections.Counter(related_objects_by_tags)

        counter_related_objects_by_tags = counter_related_objects_by_tags.most_common()

        related_objects_by_tags = [obj.pk for obj, count in counter_related_objects_by_tags]

        return self._meta.model.objects.filter(pk__in=related_objects_by_tags)
