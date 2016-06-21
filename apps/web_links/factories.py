
import random

import factory

from mylabour.utils import generate_text_by_min_length

from .models import *


class WebLinkFactory(factory.DjangoModelFactory):

    class Meta:
        model = WebLink

    @factory.lazy_attribute
    def url(self):
        url = factory.Faker('url', locale='en').generate([])
        slug_url = factory.Faker('slug').generate([])
        return url + slug_url

    @factory.lazy_attribute
    def title(self):
        if random.random() > .5:
            return ''
        return generate_text_by_min_length(10)[:50]


def web_links_factory(count):
    WebLink.objects.filter().delete()
    for i in range(count):
        WebLinkFactory()
