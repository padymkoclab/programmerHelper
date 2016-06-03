
from django.utils.text import slugify

import factory

from .constants import TAGS_NAMES
from .models import *


class TagFactory(factory.DjangoModelFactory):

    class Meta:
        model = Tag


def tags_factory(count=None):
    Tag.objects.filter().delete()
    count_tags_by_default = len(TAGS_NAMES)
    if count is None or count > count_tags_by_default:
        count = count_tags_by_default
    for tag_name in TAGS_NAMES[:count]:
        slug = slugify(tag_name, allow_unicode=True)
        TagFactory(name=slug)
