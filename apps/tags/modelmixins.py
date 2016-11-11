import collections
import itertools

from django.utils.translation import ugettext_lazy as _


class TagModelMixin(object):

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


class UserTagModelMixin(object):
    """
    """

    def get_statistics_usage_tags(self, count=None):
        """ """

        raise NotImplementedError

        tags = itertools.chain.from_iterable((
            self.solutions.values_list('tags', flat=True),
            self.snippets.values_list('tags', flat=True),
            self.questions.values_list('tags', flat=True),
            self.articles.values_list('tags', flat=True),
            self.answers.values_list('question__tags', flat=True),
        ))
        tags = collections.Counter(tags).most_common()
        tags = tuple((Tag.objects.get(pk=pk), count) for pk, count in tags)

        if count is not None:
            tags = tuple(tags)[:count]

        return tags

    def _get_couter_pks_usage_tags(self):

        all_tags_pks = itertools.chain.from_iterable((
            self.questions.values_list('tags', flat=True),
            self.snippets.values_list('tags', flat=True),
            self.solutions.values_list('tags', flat=True),
            self.articles.values_list('tags', flat=True),
        ))

        counter = collections.Counter(all_tags_pks)

        return counter

    def get_count_used_unique_tags(self):
        """ """

        if hasattr(self, 'count_used_unique_tags'):
            return self.count_used_unique_tags

        return len(self._get_couter_pks_usage_tags())
    get_count_used_unique_tags.short_description = _('Count used unique tags')
    get_count_used_unique_tags.admin_order_field = 'count_used_unique_tags'

    def get_total_count_used_tags(self):
        """ """

        if hasattr(self, 'total_count_used_tags'):
            return self.total_count_used_tags

        counter = self._get_couter_pks_usage_tags()
        return sum(counter.values())
    get_total_count_used_tags.short_description = _('Total count usaged tags')
    get_total_count_used_tags.admin_order_field = 'total_count_used_tags'

    def get_favorite_tags(self):
        """ """

        counter = self._get_couter_pks_usage_tags()

        if len(counter) == 0:
            return

        max_count = counter.most_common(1)[0][1]

        tag_pks = [tag_pk for tag_pk, count in counter.items() if count == max_count]

        return Tag._default_manager.filter(pk__in=tag_pks)
    get_favorite_tags.short_description = _('Favorite tags')
