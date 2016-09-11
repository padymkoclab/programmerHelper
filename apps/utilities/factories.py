
import random

from factory import fuzzy
import factory

from apps.comments.factories import CommentFactory
from apps.opinions.factories import OpinionFactory

from utils.django.factories_utils import (
    generate_image,
    generate_text_random_length_for_field_of_model,
    AbstractTimeStampedFactory
)

from .models import Category, Utility


class CategoryFactory(AbstractTimeStampedFactory):

    class Meta:
        model = Category

    @factory.lazy_attribute
    def name(self):
        return generate_text_random_length_for_field_of_model(self, 'name')

    @factory.lazy_attribute
    def description(self):
        return generate_text_random_length_for_field_of_model(self, 'description')

    @factory.lazy_attribute
    def image(self):
        return generate_image(filename='test_category_utilities.png', imageformat='PNG')


class UtilityFactory(AbstractTimeStampedFactory):

    class Meta:
        model = Utility

    web_link = factory.Faker('url', locale='en')

    @factory.lazy_attribute
    def category(self):
        return fuzzy.FuzzyChoice(Category.objects.all()).fuzz()

    @factory.lazy_attribute
    def name(self):
        return generate_text_random_length_for_field_of_model(self, 'name')

    @factory.lazy_attribute
    def description(self):
        return generate_text_random_length_for_field_of_model(self, 'description')

    @factory.post_generation
    def comments(self, create, extracted, **kwargs):
        for i in range(random.randrange(0, 10)):
            CommentFactory(content_object=self)

    @factory.post_generation
    def opinions(self, create, extracted, **kwargs):
        for i in range(random.randrange(0, 10)):
            OpinionFactory(content_object=self)

    @factory.post_generation
    def date_added(self, create, extracted, **kwargs):
        self.date_added = fuzzy.FuzzyDateTime(self.category.date_added).fuzz()
        self.save()
