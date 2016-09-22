
import random

from django.utils import timezone

import factory
from factory import fuzzy

from utils.django.factories_utils import generate_text_random_length_for_field_of_model

from .models import User, Level, Profile


class LevelFactory(factory.DjangoModelFactory):

    class Meta:
        model = Level


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = User

    email = factory.Faker('email', 'en')
    username = factory.Faker('user_name', 'ru')
    display_name = factory.Faker('name', 'ru')

    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')

    profile = factory.RelatedFactory('apps.users.factories.ProfileFactory', 'user')
    diary = factory.RelatedFactory('apps.diaries.factories.DiaryFactory', 'user')

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

    @factory.post_generation
    def date_joined(self, created, extracted, **kwargs):
        self.date_joined = fuzzy.FuzzyDateTime(timezone.now() - timezone.timedelta(weeks=60)).fuzz()
        self.save()


class ProfileFactory(factory.DjangoModelFactory):

    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory, profile=None)
    views = fuzzy.FuzzyInteger(0, 1000)
    gender = fuzzy.FuzzyChoice([val for val, label in Profile.CHOICES_GENDER])

    @factory.lazy_attribute
    def about(self):
        if random.random() > .5:
            return generate_text_random_length_for_field_of_model(self, 'about')
        return ''

    @factory.lazy_attribute
    def presents_on_gmail(self):
        if random.random() > .5:
            return'https://google.com/' + factory.Faker('user_name').generate([]).lower()
        return ''

    @factory.lazy_attribute
    def presents_on_github(self):
        if random.random() > .5:
            return'https://github.com/' + factory.Faker('user_name').generate([]).lower()
        return ''

    @factory.lazy_attribute
    def presents_on_stackoverflow(self):
        if random.random() > .5:
            return'https://stackoverflow.com/' + factory.Faker('user_name').generate([]).lower()
        return ''

    @factory.lazy_attribute
    def signature(self):
        if random.random() > .5:
            return generate_text_random_length_for_field_of_model(self, 'signature')
        return ''

    @factory.lazy_attribute
    def personal_website(self):
        if random.random() > .5:
            return factory.Faker('url').generate([])
        return ''

    @factory.lazy_attribute
    def date_birthday(self):
        if random.random() > .5:
            return fuzzy.FuzzyDate(
                timezone.now() - timezone.timedelta(days=20000),
                timezone.now()
            ).fuzz()
        return

    @factory.lazy_attribute
    def longitude(self):
        if random.random() > .5:
            return factory.Faker('longitude').generate([])
        return

    @factory.lazy_attribute
    def latitude(self):
        if random.random() > .5:
            return factory.Faker('latitude').generate([])
        return

    @factory.lazy_attribute
    def real_name(self):
        if random.random() > .5:
            return factory.Faker('name', 'ru').generate([])
        return ''

    @factory.lazy_attribute
    def location(self):
        if random.random() > .5:
            city = factory.Faker('city').generate([])
            country = factory.Faker('country').generate([])
            return '{}, {}'.format(city, country)
        return ''

    @factory.lazy_attribute
    def phone(self):
        if random.random() > .5:
            return factory.Faker('phone_number').generate([])
        return ''

    @factory.lazy_attribute
    def job(self):
        if random.random() > .5:
            if random.random() > .5:
                return factory.Faker('company').generate([])
            return 'Freelance'
        return ''
