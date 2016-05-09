
import random

from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from apps.app_generic_models.factories import Factory_UserComment_Generic, Factory_UserOpinion_Generic

from .models import *


Accounts = get_user_model().objects.all()


class Factory_Cource(factory.DjangoModelFactory):

    class Meta:
        model = Course

    description = factory.Faker('text', locale='ru')

    @factory.lazy_attribute
    def name(self):
        return factory.Faker('text', locale='ru').generate([])[:30]

    @factory.lazy_attribute
    def picture(self):
        site_name = factory.Faker('url', locale='ru').generate([])
        picture_name = factory.Faker('slug', locale='ru').generate([])
        return '{0}{1}.png'.format(site_name, picture_name)

    @factory.lazy_attribute
    def lexer(self):
        return fuzzy.FuzzyChoice(CHOICES_LEXERS).fuzz()[0]


class Factory_Lesson(factory.DjangoModelFactory):

    class Meta:
        model = Lesson

    header = factory.Faker('text', locale='ru')
    conclusion = factory.Faker('text', locale='ru')
    number = factory.Sequence(lambda n: n)

    @factory.lazy_attribute
    def name(self):
        return factory.Faker('text', locale='ru').generate([])[:30]

    @factory.lazy_attribute
    def is_completed(self):
        if divmod(random.random(), 0.1)[0] > 7:
            return False
        return True


class Factory_Sublesson(factory.DjangoModelFactory):

    class Meta:
        model = Sublesson

    text = factory.Faker('text', locale='ru')
    code = factory.Faker('text', locale='ru')
    number = factory.Sequence(lambda n: n)

    @factory.lazy_attribute
    def title(self):
        return factory.Faker('text', locale='ru').generate([])[:30]


Course.objects.filter().delete()
# create courses
for i in range(10):
    course = Factory_Cource()
    random_count_authors = random.randint(1, 3)
    accounts = random.sample(tuple(Accounts), random_count_authors)
    course.authorship.set = accounts
    # create lessons
    for j in range(random.randint(Course.MIN_COUNT_LESSONS, Course.MAX_COUNT_LESSONS)):
        lesson = Factory_Lesson(course=course)
        for e in range(random.randint(0, 10)):
            Factory_UserComment_Generic(content_object=lesson)
        for k in range(random.randint(0, 10)):
            Factory_UserOpinion_Generic(content_object=lesson)
        # create sublessons
        for q in range(random.randint(Lesson.MIN_COUNT_SUBLESSONS, Lesson.MAX_COUNT_SUBLESSONS)):
            Factory_Sublesson(lesson=lesson)
