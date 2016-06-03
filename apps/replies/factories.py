
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from .models import Reply


class ReplyFactory(factory.DjangoModelFactory):

    class Meta:
        model = Reply

    text_reply = factory.Faker('text', locale='ru')
    scope_for_content = fuzzy.FuzzyInteger(5)
    scope_for_style = fuzzy.FuzzyInteger(5)
    scope_for_language = fuzzy.FuzzyInteger(5)

    @factory.lazy_attribute
    def account(self):
        users_given_their_replies = self.content_object.replies.values('account')
        users_given_not_their_replies = get_user_model().objects.exclude(pk__in=users_given_their_replies)
        if not users_given_not_their_replies.count():
            type_instance = self.content_object._meta.verbose_name.lower()
            msg = _('All users given their reply about {0} "{1.content_object}"').format(type_instance, self)
            raise ValueError(msg)
        return users_given_not_their_replies.random_accounts(1)

    @factory.lazy_attribute
    def impress(self):
        return factory.Faker('text', locale='ru').generate([])[:50]

    @factory.lazy_attribute
    def advantages(self):
        words = factory.Faker('text', locale='ru').generate([]).split(' ')
        words = words[:8]
        return ', '.join(word.strip().title() for word in words)

    @factory.lazy_attribute
    def disadvantages(self):
        words = factory.Faker('text', locale='ru').generate([]).split(' ')
        words = words[:8]
        return ', '.join(word.strip().title() for word in words)
