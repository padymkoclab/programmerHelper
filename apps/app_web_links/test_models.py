
import factory

from .models import *


class Factory_WebLink(factory.DjangoModelFactory):

    class Meta:
        model = WebLink

    @factory.lazy_attribute
    def web_url(self):
        url = factory.Faker('url', locale='ru').generate([])
        slug_url = factory.Faker('slug', locale='ru').generate([])
        return url + slug_url

    @factory.lazy_attribute
    def title(self):
        name_ru = factory.Faker('text', locale='ru').generate([])[:25]
        name_en = factory.Faker('text', locale='en').generate([])[:25]
        return '{0} {1}'.format(name_en, name_ru)


for i in range(500):
    Factory_WebLink()
