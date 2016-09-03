
from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from mylabour.factories_utils import generate_text_random_length_for_field_of_model

from .models import Comment


class CommentFactory(factory.DjangoModelFactory):

    class Meta:
        model = Comment

    @factory.lazy_attribute
    def text_comment(self):
        return generate_text_random_length_for_field_of_model(self, 'text_comment')

    @factory.lazy_attribute
    def user(self):
        return fuzzy.FuzzyChoice(get_user_model()._default_manager.all()).fuzz()
