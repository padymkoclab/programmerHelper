
import random
import inspect

from django.utils import timezone

from factory import fuzzy
import factory

from apps.comments.factories import CommentFactory
from apps.opinions.factories import OpinionFactory

from mylabour.factories_utils import generate_image, generate_text_certain_length

from .models import UtilityCategory, Utility


NOW = timezone.now().replace(tzinfo=timezone.get_current_timezone())


def generate_text_random_length_for_field(model, field_name, ending_point=True, locale='ru'):

    field = model._meta.get_field(field_name)

    for validator in field.validators:
        if validator.code == 'min_length':
            min_length = validator.limit_value
        elif validator.code == 'max_length':
            max_length = validator.limit_value

    length = random.randrange(min_length, max_length)

    if ending_point:
        return generate_text_certain_length(length + 1, locale)[:-1]
    return generate_text_certain_length(length, locale)


class UtilityCategoryFactory(factory.DjangoModelFactory):

    class Meta:
        model = UtilityCategory

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        super(UtilityCategoryFactory, cls)._after_postgeneration(obj, create, results)
        qs = obj.__class__._default_manager.filter(pk=obj.pk)
        qs.update(date_modified=fuzzy.FuzzyDateTime(obj.date_added, NOW).fuzz())

    @factory.lazy_attribute
    def name(self):

        field_name = inspect.stack()[0][3]
        model = self._LazyStub__model_class._meta.model
        return generate_text_random_length_for_field(model, field_name, ending_point=False)

    @factory.lazy_attribute
    def description(self):

        field_name = inspect.stack()[0][3]
        model = self._LazyStub__model_class._meta.model
        return generate_text_random_length_for_field(model, field_name)

    @factory.lazy_attribute
    def image(self):
        return generate_image(filename='test_category_utilities.png', imageformat='PNG')

    @factory.post_generation
    def date_added(self, create, extracted, **kwargs):
        self.date_added = fuzzy.FuzzyDateTime(NOW - timezone.timedelta(days=500)).fuzz()
        self.save()


class UtilityFactory(factory.DjangoModelFactory):

    class Meta:
        model = Utility

    category = fuzzy.FuzzyChoice(UtilityCategory.objects.all())
    web_link = factory.Faker('url', locale='en')

    @factory.lazy_attribute
    def name(self):
        field_name = inspect.stack()[0][3]
        model = self._LazyStub__model_class._meta.model
        return generate_text_random_length_for_field(model, field_name, ending_point=False)

    @factory.lazy_attribute
    def description(self):
        field_name = inspect.stack()[0][3]
        model = self._LazyStub__model_class._meta.model
        return generate_text_random_length_for_field(model, field_name)

    @factory.post_generation
    def comments(self, create, extracted, **kwargs):
        for i in range(random.randrange(0, 10)):
            CommentFactory(content_object=self)

    @factory.post_generation
    def opinions(self, create, extracted, **kwargs):
        for i in range(random.randrange(0, 10)):
            OpinionFactory(content_object=self)
