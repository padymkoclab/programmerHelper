
import factory
from factory import fuzzy

from utils.django.factories_utils import generate_text_random_length_for_field_of_model, AbstractTimeStampedFactory

from .models import Poll, Choice


class PollFactory(AbstractTimeStampedFactory):

    class Meta:
        model = Poll

    status = fuzzy.FuzzyChoice([value for value, label in Poll.CHOICES_STATUS])

    @factory.lazy_attribute
    def title(self):
        return generate_text_random_length_for_field_of_model(self, 'title')

    @factory.lazy_attribute
    def description(self):
        return generate_text_random_length_for_field_of_model(self, 'description')


class ChoiceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Choice

    @factory.lazy_attribute
    def text_choice(self):
        return generate_text_random_length_for_field_of_model(self, 'text_choice')
