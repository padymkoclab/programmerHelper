
import random

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

import factory

from .models import Mark


class MarkFactory(factory.DjangoModelFactory):

    class Meta:
        model = Mark

    @factory.lazy_attribute
    def mark(self):
        return random.randint(Mark.MIN_MARK, Mark.MAX_MARK)

    @factory.lazy_attribute
    def account(self):
        users_already_given_their_marks = self.content_object.marks.values('account')
        authors_labour_pk = [self.content_object.account.pk]
        users_given_not_mark_yet = get_user_model().objects.exclude(pk__in=users_already_given_their_marks)
        users_given_not_mark_yet_and_no_authors = users_given_not_mark_yet.exclude(pk__in=authors_labour_pk)
        if not users_given_not_mark_yet_and_no_authors.count():
            msg = _('All users already given their marks about {0} "{1}"').format(
                self.content_object._meta.verbose_name.lower(),
                self.content_object.__str__()
            )
            raise ValueError(msg)
        return users_given_not_mark_yet_and_no_authors.random_accounts(1)
