
import random

import factory

from .models import *


class Factory_Account(factory.DjangoModelFactory):

    class Meta:
        model = Account

    email = factory.Faker('email', locale='ru')
    username = factory.Faker('name', locale='ru')
    date_birthday = factory.Faker('date', locale='ru')
    real_name = factory.Faker('first_name', locale='ru')

    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')

    @factory.lazy_attribute
    def gender(self):
        return random.choice(tuple(Account.CHOICES_GENDER._db_values))

    @factory.lazy_attribute
    def account_type(self):
        random_float_number = random.random()
        if random_float_number >= 0.9:
            return Account.CHOICES_ACCOUNT_TYPES.platinum
        elif 0.7 <= random_float_number < 0.9:
            return Account.CHOICES_ACCOUNT_TYPES.golden
        else:
            return Account.CHOICES_ACCOUNT_TYPES.regular

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


for i in range(100):
    Factory_Account()
