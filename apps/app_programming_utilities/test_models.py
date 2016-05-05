
from factory import fuzzy
import factory

from .models import *


class Factory_ProgrammingCategory(factory.DjangoModelFactory):

    class Meta:
        model = ProgrammingCategory

    description = factory.Faker('text', locale='ru')

    @factory.lazy_attribute
    def name(self):
        return factory.Faker('text', locale='ru').generate([])[:40]

    @factory.lazy_attribute
    def picture(self):
        site_url = factory.Faker('url', locale='ru').generate([])
        picture_url = factory.Faker('slug', locale='ru').generate([])
        return site_url + picture_url + '.png'


class Factory_ProgrammingUtility(factory.DjangoModelFactory):

    class Meta:
        model = ProgrammingUtility

    description = factory.Faker('text', locale='ru')
    url_in_web = factory.Faker('url', locale='ru')
    category = fuzzy.FuzzyChoice(ProgrammingCategory.objects.all())

    @factory.lazy_attribute
    def name(self):
        return factory.Faker('text', locale='ru').generate([])[:40]
