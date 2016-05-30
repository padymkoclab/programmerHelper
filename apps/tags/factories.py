
from django.utils.text import slugify

import factory

from .constants import TAGS_NAMES
from .models import *


class Factory_Tag(factory.DjangoModelFactory):

    class Meta:
        model = Tag


def factory_tags(count=None):
    Tag.objects.filter().delete()
    count_tags_by_default = len(TAGS_NAMES)
    if count is None or count > count_tags_by_default:
        count = count_tags_by_default
    for tag_name in TAGS_NAMES[:count]:
        slug = slugify(tag_name, allow_unicode=True)
        Factory_Tag(name=slug)
