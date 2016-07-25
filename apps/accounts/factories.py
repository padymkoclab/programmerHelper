
import random

from django.utils import timezone
from django.utils.text import slugify

import factory
from factory import fuzzy

from .models import Account, AccountLevel


class AccountLevelFactory(factory.DjangoModelFactory):

    class Meta:
        model = AccountLevel


class AccountFactory(factory.DjangoModelFactory):

    class Meta:
        model = Account

    email = factory.Faker('email', locale='en')
    username = factory.Faker('name', locale='en')
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
        return 'http://google.com/accounts/{0}'.format(slug_name)

    @factory.lazy_attribute
    def presents_on_github(self):
        slug_name = self.username.lower().replace(' ', '_')
        return 'http://github.com/{0}'.format(slug_name)

    @factory.lazy_attribute
    def presents_on_stackoverflow(self):
        slug_name = self.username.lower().replace(' ', '_')
        return 'http://stackoverflow.com/accounts/{0}'.format(slug_name)

    @factory.lazy_attribute
    def personal_website(self):
        slug_name = slugify(self.username, allow_unicode=True)
        return 'http://{0}.com'.format(slug_name)

    @factory.lazy_attribute
    def signature(self):
        return 'Sincerely {0.username}'.format(self)

    @factory.post_generation
    def date_joined(self, created, extracted, **kwargs):
        self.date_joined = fuzzy.FuzzyDateTime(timezone.now() - timezone.timedelta(weeks=60)).fuzz()
        self.save()
