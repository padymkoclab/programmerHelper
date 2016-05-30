
from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from .models import Comment


class Factory_Comment(factory.DjangoModelFactory):

    class Meta:
        model = Comment

    text_comment = factory.Faker('text', locale='ru')
    account = fuzzy.FuzzyChoice(get_user_model().objects.all())
