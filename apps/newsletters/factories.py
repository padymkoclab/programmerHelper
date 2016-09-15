
from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from utils.django.factories_utils import generate_text_random_length_for_field_of_model

from .models import Newsletter


class NewsletterFactory(factory.DjangoModelFactory):

    class Meta:
        model = Newsletter

    @factory.lazy_attribute
    def content(self):

        return generate_text_random_length_for_field_of_model(self, 'content')

    @factory.lazy_attribute
    def user(self):

        return fuzzy.FuzzyChoice(get_user_model().objects.all()).fuzz()

    @factory.post_generation
    def date_added(self, create, extracted, **kwargs):

        self.date_added = fuzzy.FuzzyDateTime(self.user.date_joined).fuzz()
        self.save()
