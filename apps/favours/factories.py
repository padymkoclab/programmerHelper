
from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from .models import Favour


class Factory_Favour(factory.DjangoModelFactory):

    class Meta:
        model = Favour

    is_favour = fuzzy.FuzzyChoice([True, False])

    @factory.lazy_attribute
    def account(self):
        already_given_his_favours_users = self.content_object.favours.values('account')
        author_labour = self.content_object.account
        users_yet_not_his_favours = get_user_model().objects.exclude(pk__in=already_given_his_favours_users)
        users_yet_not_his_favours_and_no_author = users_yet_not_his_favours.exclude(pk=author_labour.pk)
        if not users_yet_not_his_favours_and_no_author.count():
            msg = 'All users already given his favour about {0} "{1}"'.format(
                self.content_object._meta.verbose_name.lower(),
                self.content_object.__str__()
            )
            raise ValueError(msg)
        return users_yet_not_his_favours_and_no_author.random_accounts(1)
