
import random

from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from apps.generic_models.factories import Factory_CommentGeneric, Factory_OpinionGeneric

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
    views = fuzzy.FuzzyInteger(1000)

    @factory.lazy_attribute
    def name(self):
        return factory.Faker('text', locale='ru').generate([])[:30]

    @factory.lazy_attribute
    def is_completed(self):
        if divmod(random.random(), 0.1)[0] > 7:
            return False
        return True

    @factory.post_generation
    def comments(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 3)):
            Factory_CommentGeneric(content_object=self)

    @factory.post_generation
    def opinions(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 5)):
            Factory_OpinionGeneric(content_object=self)


class Factory_Sublesson(factory.DjangoModelFactory):

    class Meta:
        model = Sublesson

    text = factory.Faker('text', locale='ru')
    code = factory.Faker('text', locale='ru')

    @factory.lazy_attribute
    def title(self):
        return factory.Faker('text', locale='ru').generate([])[:30]


def factory_courses(count):
    Course.objects.filter().delete()
    # create courses
    for i in range(count):
        course = Factory_Cource()
        random_count_authors = random.randint(1, Course.MAX_COUNT_AUTHORS)
        accounts = random.sample(tuple(Accounts), random_count_authors)
        course.authorship.set(accounts)
        # create lessons
        for number_lesson, j in enumerate(range(random.randint(Course.MIN_COUNT_LESSONS, Course.MAX_COUNT_LESSONS))):
            lesson = Factory_Lesson(course=course, number=number_lesson + 1)
            # create sublessons
            for number_sublesson, q in enumerate(range(random.randint(Lesson.MIN_COUNT_SUBLESSONS, Lesson.MAX_COUNT_SUBLESSONS))):
                Factory_Sublesson(lesson=lesson, number=number_sublesson + 1)
