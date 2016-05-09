
from factory import fuzzy
import factory

from apps.app_generic_models.factories import Factory_UserComment_Generic, Factory_UserOpinion_Generic

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
    picture = factory.Faker('url', locale='ru')
    category = fuzzy.FuzzyChoice(ProgrammingCategory.objects.all())

    @factory.lazy_attribute
    def name(self):
        return factory.Faker('text', locale='ru').generate([])[:40]


ProgrammingCategory.objects.filter().delete()
# create category
for i in range(10):
    category = Factory_ProgrammingCategory()
    # create utility
    for j in range(random.randrange(10)):
        utility = Factory_ProgrammingUtility(category=category)
        # create comments
        for e in range(random.randrange(10)):
            Factory_UserComment_Generic(content_object=utility)
        # create opinions
        for k in range(random.randrange(10)):
            Factory_UserOpinion_Generic(content_object=utility)
