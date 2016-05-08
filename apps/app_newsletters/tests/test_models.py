
from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from .models import *


class Factory_Newsletter(factory.DjangoModelFactory):

    class Meta:
        model = Newsletter

    author = fuzzy.FuzzyChoice(get_user_model().objects.all())

    @factory.lazy_attribute
    def title(self):
        return factory.Faker('text', locale='ru').generate([])[:50]

    @factory.lazy_attribute
    def content(self):
        content = list()
        for i in range(10):
            content.append(factory.Faker('text', locale='ru').generate([]))
        return '. '.join(content)

    @factory.lazy_attribute
    def web_link(self):
        site_name = factory.Faker('url', locale='ru').generate([])
        link_name = factory.Faker('slug', locale='ru').generate([])
        web_link = '{0}{1}.html'.format(site_name, link_name)
        return web_link

Newsletter.objects.filter().delete()
for i in range(20):
    Factory_Newsletter()
