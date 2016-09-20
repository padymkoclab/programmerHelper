
import factory

from utils.django.factories_utils import generate_text_random_length_for_field_of_model

from .models import Tag


class TagFactory(factory.DjangoModelFactory):

    class Meta:
        model = Tag

    @factory.lazy_attribute
    def description(self):
        return generate_text_random_length_for_field_of_model(self, 'description')
