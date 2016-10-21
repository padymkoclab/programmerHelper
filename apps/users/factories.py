
import uuid
import random

from django.utils.text import slugify
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
    alias = factory.Faker('name', 'ru')

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
    def on_gmail(self):
        if random.random() > .5:
            return str(uuid.uuid1().int)[:21]
        return ''

    @factory.lazy_attribute
    def on_github(self):
        if random.random() > .5:
            return slugify(factory.Faker('name').generate([]))
        return ''

    @factory.lazy_attribute
    def on_stackoverflow(self):
        if random.random() > .5:
            user_id = random.sample(str(uuid.uuid1().int), random.randint(5, 10))
            user_id = ''.join(user_id)
            user_name = slugify(factory.Faker('name').generate([]))
            return '{}/{}'.format(user_id, user_name)
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
        return factory.Faker('longitude').generate([])

    @factory.lazy_attribute
    def latitude(self):
        return factory.Faker('latitude').generate([])

    @factory.lazy_attribute
    def real_name(self):
        if random.random() > .5:
            return factory.Faker('name', 'ru').generate([])
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
