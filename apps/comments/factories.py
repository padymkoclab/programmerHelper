
from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from .models import Comment


class CommentFactory(factory.DjangoModelFactory):

    class Meta:
        model = Comment

    user = fuzzy.FuzzyChoice(get_user_model()._default_manager.all())

    @factory.lazy_attribute
    def text_comment(self):
        return factory.Faker('text', locale='ru')
