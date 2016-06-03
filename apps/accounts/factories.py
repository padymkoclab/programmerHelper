
import random

import factory
from factory import fuzzy

from .models import *


class AccountLevelFactory(factory.DjangoModelFactory):

    class Meta:
        model = AccountLevel


class AccountFactory(factory.DjangoModelFactory):

    class Meta:
        model = Account

    email = factory.Faker('email', locale='ru')
    username = factory.Faker('name', locale='ru')
    date_birthday = factory.Faker('date', locale='ru')
    real_name = factory.Faker('first_name', locale='ru')
    gender = fuzzy.FuzzyChoice(Account.CHOICES_GENDER._db_values)

    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')

    @factory.lazy_attribute
    def is_active(self):
        random_float_number = random.random()
        if random_float_number >= 0.9:
            return False
        else:
            return True

    @factory.lazy_attribute
    def is_superuser(self):
        random_float_number = random.random()
        if random_float_number >= 0.95:
            return True
        else:
            return False

    @factory.lazy_attribute
    def presents_on_gmail(self):
        slug_name = self.username.lower().replace(' ', '_')
        return 'http://google/accounts/{0}'.format(slug_name)

    @factory.lazy_attribute
    def presents_on_github(self):
        slug_name = self.username.lower().replace(' ', '_')
        return 'http://github/{0}'.format(slug_name)

    @factory.lazy_attribute
    def presents_on_stackoverflow(self):
        slug_name = self.username.lower().replace(' ', '_')
        return 'http://stackoverflow/accounts/{0}'.format(slug_name)

    @factory.lazy_attribute
    def personal_website(self):
        slug_name = self.username.lower().replace(' ', '_')
        return 'http://{0}.com'.format(slug_name)


def account_level_factory():
    AccountLevel.objects.filter().delete()
    AccountLevelFactory(name=AccountLevel.CHOICES_LEVEL.platinum, color='#D8BFD8', description='Regular level of account')
    AccountLevelFactory(name=AccountLevel.CHOICES_LEVEL.golden, color='#FFD700', description='Golder level of account')
    AccountLevelFactory(name=AccountLevel.CHOICES_LEVEL.silver, color='#C0C0C0', description='Silver level of account')
    AccountLevelFactory(name=AccountLevel.CHOICES_LEVEL.diamond, color='#4B0082', description='Diamond level of account')
    AccountLevelFactory(name=AccountLevel.CHOICES_LEVEL.ruby, color='#DC143C', description='Ruby level of account')
    AccountLevelFactory(name=AccountLevel.CHOICES_LEVEL.sapphire, color='#483D8B', description='Sapphire level of account')
    AccountLevelFactory(name=AccountLevel.CHOICES_LEVEL.malachite, color='#3CB371', description='Malachite level of account')
    AccountLevelFactory(name=AccountLevel.CHOICES_LEVEL.amethyst, color='#800080', description='Amethyst level of account')
    AccountLevelFactory(name=AccountLevel.CHOICES_LEVEL.emerald, color='#00FA9A', description='Emerald level of account')
    AccountLevelFactory(name=AccountLevel.CHOICES_LEVEL.agate, color='#2F4F4F', description='Agate level of account')
    AccountLevelFactory(name=AccountLevel.CHOICES_LEVEL.turquoise, color='#40E0D0', description='Turquoise level of account')
    AccountLevelFactory(name=AccountLevel.CHOICES_LEVEL.amber, color='#FF8C00', description='Amber level of account')
    AccountLevelFactory(name=AccountLevel.CHOICES_LEVEL.opal, color='#FF7F50', description='Opal level of account')
    AccountLevelFactory(name=AccountLevel.CHOICES_LEVEL.regular, color='#F0F8FF', description='Regular level of account')


def accounts_factory(count):
    if not AccountLevel.objects.count() and count > 0:
        account_level_factory()
    for i in range(count):
        AccountFactory()
