
import random

from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from mylabour.models import OpinionUserModel

from .models import *


Accounts = get_user_model().objects.all()


class Factory_Snippet(factory.DjangoModelFactory):

    class Meta:
        model = Snippet

    author = fuzzy.FuzzyChoice(Accounts)
    description = factory.Faker('text', locale='ru')
    code = factory.Faker('text', locale='en')

    @factory.lazy_attribute
    def title(self):
        return factory.Faker('text', locale='ru').generate([])[:30]

    @factory.lazy_attribute
    def lexer(self):
        return random.choice(CHOICES_LEXERS)[0]


class Factory_OpinionAboutSnippet(factory.DjangoModelFactory):

    class Meta:
        model = OpinionAboutSnippet

    is_useful = fuzzy.FuzzyChoice([True, False, None])

    @factory.lazy_attribute
    def is_favorite(self):
        if self.is_useful is None:
            return OpinionUserModel.CHOICES_FAVORITE.unknown
        return random.choice(tuple(OpinionUserModel.CHOICES_FAVORITE._db_values))


class Factory_SnippetComment(factory.DjangoModelFactory):

    class Meta:
        model = SnippetComment

    snippet = fuzzy.FuzzyChoice(Snippet.objects.all())
    author = fuzzy.FuzzyChoice(Accounts)
    text_comment = factory.Faker('text', locale='ru')


Snippet.objects.filter().delete()
for i in range(50):
    snippet = Factory_Snippet()
    random_count_comments = random.randrange(0, 5)
    random_count_users = random.randrange(0, len(Accounts))
    random_count_tags = random.randrange(Tag.MIN_COUNT_TAGS_ON_OBJECT, Tag.MAX_COUNT_TAGS_ON_OBJECT + 1)
    if random_count_tags > Tag.objects.count():
        random_count_tags = Tag.objects.count()
    users = random.sample(tuple(Accounts), random_count_users)
    tags = random.sample(tuple(Tag.objects.all()), random_count_tags)
    snippet.tags.set(tags)
    for user in users:
        Factory_OpinionAboutSnippet(user=user, snippet=snippet)
    for i in range(random_count_comments):
        Factory_SnippetComment(snippet=snippet)
