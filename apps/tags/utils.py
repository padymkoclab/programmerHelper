
import collections

from .models import Tag


def get_favorite_tags(qs_tags_pks):

    if not qs_tags_pks.exists():
        return Tag.objects.none()

    counter_pks_tags = collections.Counter(qs_tags_pks)

    max_counter_pks_tags = max(counter_pks_tags.values())

    filter_max_pks_tags = filter(lambda x: x[1] == max_counter_pks_tags, counter_pks_tags.items())
    pks_tags = dict(filter_max_pks_tags).keys()

    tags = Tag.objects.filter(pk__in=pks_tags)

    return tags
