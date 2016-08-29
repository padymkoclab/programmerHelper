
from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from .models import Opinion


class OpinionFactory(factory.DjangoModelFactory):

    class Meta:
        model = Opinion

    is_useful = fuzzy.FuzzyChoice([True, False])

    @factory.lazy_attribute
    def user(self):

        already_have_opinions_users = self.content_object.opinions.values('user')

        users_without_opinions = get_user_model()._default_manager.exclude(pk__in=already_have_opinions_users)

        if hasattr(self.content_object, 'user'):
            author_labour = self.content_object.user
            users_without_opinions = users_without_opinions.exclude(pk=author_labour.pk)

        if not users_without_opinions.count():
            msg = 'All users have opinions about {0} "{1}"'.format(
                self.content_object._meta.verbose_name.lower(),
                self.content_object.__str__()
            )
            raise ValueError(msg)

        return users_without_opinions.random_users(1)
