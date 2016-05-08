
import factory

from .models import *


class Factory_Tag(factory.DjangoModelFactory):

    class Meta:
        model = Tag

    @factory.lazy_attribute
    def name(self):
        random_name_ru = factory.Faker('first_name', locale='ru').generate([])
        random_name_en = factory.Faker('first_name', locale='en').generate([])
        return '{0} {1}'.format(random_name_ru, random_name_en)[:30]


Tag.objects.filter().delete()
for i in range(300):
    Factory_Tag()
