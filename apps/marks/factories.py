
import random

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
    def user(self):

        users_already_given_their_marks = self.content_object.marks.values('user')
        authors_labour_pk = [self.content_object.user.pk]
        users_given_not_mark_yet = get_user_model().objects.exclude(pk__in=users_already_given_their_marks)
        users_given_not_mark_yet_and_no_authors = users_given_not_mark_yet.exclude(pk__in=authors_labour_pk)
        return users_given_not_mark_yet_and_no_authors.first()
