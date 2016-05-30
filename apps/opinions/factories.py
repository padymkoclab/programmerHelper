
from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from .models import Opinion


class Factory_Opinion(factory.DjangoModelFactory):

    class Meta:
        model = Opinion

    is_useful = fuzzy.FuzzyChoice([True, False])

    @factory.lazy_attribute
    def account(self):
        already_have_opinions_users = self.content_object.opinions.values('account')
        author_labour = self.content_object.account
        users_without_opinions = get_user_model().objects.exclude(pk__in=already_have_opinions_users)
        users_without_opinions_and_no_author = users_without_opinions.exclude(pk=author_labour.pk)
        if not users_without_opinions_and_no_author.count():
            msg = 'All users have opinions about {0} "{1}"'.format(
                self.content_object._meta.verbose_name.lower(),
                self.content_object.__str__()
            )
            raise ValueError(msg)
        return users_without_opinions_and_no_author.random_accounts(1)
