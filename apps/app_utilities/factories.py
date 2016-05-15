
import random

from factory import fuzzy
import factory

from apps.app_generic_models.factories import Factory_CommentGeneric, Factory_OpinionGeneric

from .models import *


class Factory_UtilityCategory(factory.DjangoModelFactory):

    class Meta:
        model = UtilityCategory

    description = factory.Faker('text', locale='ru')
    views = fuzzy.FuzzyInteger(1000)

    @factory.lazy_attribute
    def name(self):
        return factory.Faker('text', locale='ru').generate([])[:40]

    @factory.lazy_attribute
    def picture(self):
        site_url = factory.Faker('url', locale='ru').generate([])
        picture_url = factory.Faker('slug', locale='ru').generate([])
        return site_url + picture_url + '.png'


class Factory_Utility(factory.DjangoModelFactory):

    class Meta:
        model = Utility

    description = factory.Faker('text', locale='ru')
    picture = factory.Faker('url', locale='ru')
    category = fuzzy.FuzzyChoice(UtilityCategory.objects.all())
    web_link = factory.Faker('url', locale='en')

    @factory.lazy_attribute
    def name(self):
        return factory.Faker('text', locale='ru').generate([])[:40]

    @factory.post_generation
    def comments(self, create, extracted, **kwargs):
        for i in range(random.randrange(3)):
            Factory_CommentGeneric(content_object=self)

    @factory.post_generation
    def opinions(self, create, extracted, **kwargs):
        for i in range(random.randrange(10)):
            Factory_OpinionGeneric(content_object=self)


UtilityCategory.objects.filter().delete()
# create category
for i in range(10):
    Factory_UtilityCategory()
# create utility
for j in range(30):
    Factory_Utility()
