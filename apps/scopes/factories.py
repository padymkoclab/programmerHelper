
import random

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

import factory

from .models import Scope


class ScopeFactory(factory.DjangoModelFactory):

    class Meta:
        model = Scope

    @factory.lazy_attribute
    def scope(self):
        return random.randint(Scope.MIN_SCOPE, Scope.MAX_SCOPE)

    @factory.lazy_attribute
    def account(self):
        users_already_given_their_scopes = self.content_object.scopes.values('account')
        authors_labour_pk = [self.content_object.account.pk]
        users_given_not_scope_yet = get_user_model().objects.exclude(pk__in=users_already_given_their_scopes)
        users_given_not_scope_yet_and_no_authors = users_given_not_scope_yet.exclude(pk__in=authors_labour_pk)
        if not users_given_not_scope_yet_and_no_authors.count():
            msg = _('All users already given their scopes about {0} "{1}"').format(
                self.content_object._meta.verbose_name.lower(),
                self.content_object.__str__()
            )
            raise ValueError(msg)
        return users_given_not_scope_yet_and_no_authors.random_accounts(1)
