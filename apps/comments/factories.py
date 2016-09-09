
from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from utils.django.factories_utils import generate_text_random_length_for_field_of_model, AbstractTimeStampedFactory

from .models import Comment


class CommentFactory(AbstractTimeStampedFactory):

    class Meta:
        model = Comment

    @factory.lazy_attribute
    def text_comment(self):
        return generate_text_random_length_for_field_of_model(self, 'text_comment')

    @factory.lazy_attribute
    def user(self):
        return fuzzy.FuzzyChoice(get_user_model()._default_manager.all()).fuzz()

    @factory.post_generation
    def date_added(self, create, exctracted, **kwargs):
        self.date_added = fuzzy.FuzzyDateTime(self.user.date_joined).fuzz()
        self.save()
