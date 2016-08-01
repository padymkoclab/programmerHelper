
import factory
from factory import fuzzy

from mylabour.factories_utils import generate_text_by_min_length

from .models import Poll, Choice


class PollFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Poll

    status = fuzzy.FuzzyChoice(Poll.CHOICES_STATUS._db_values)

    @factory.lazy_attribute
    def title(self):
        return factory.Faker('text', locale='ru').generate([])[:50]

    @factory.lazy_attribute
    def description(self):
        return generate_text_by_min_length(10)[:100]


class ChoiceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Choice

    poll = fuzzy.FuzzyChoice(Poll.objects.opened_polls())
    text_choice = factory.Faker('text', locale='ru')
