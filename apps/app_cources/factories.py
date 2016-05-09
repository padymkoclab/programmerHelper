
# import datetime
import random

from django.contrib.auth import get_user_model
from django.conf import settings

import factory
from factory import fuzzy

from apps.app_generic_models.factories import Factory_UserComment_Generic, Factory_UserOpinion_Generic

from .models import *

Accounts = get_user_model().objects.all()


class Factory_Cource(factory.DjangoModelFactory):

    class Meta:
        model = Course

    description = factory.Faker('text', locale='ru')

    @factory.lazy_attribute
    def name(self):
        return factory.Faker('text', locale='ru').generate([])[:30]

    @factory.lazy_attribute
    def picture(self):
        site_name = factory.Faker('url', locale='ru').generate([])
        picture_name = factory.Faker('slug', locale='ru').generate([])
        return '{0}{1}.png'.format(site_name, picture_name)

    @factory.lazy_attribute
    def lexer(self):
        return fuzzy.FuzzyChoice(CHOICES_LEXERS).fuzz()[0]

Course.objects.filter().delete()
for i in range(10):
    cource = Factory_Cource()
    random_count_authors = random.randint(1, 3)
    accounts = random.sample(tuple(Accounts), random_count_authors)
    cource.authorship.set = accounts
