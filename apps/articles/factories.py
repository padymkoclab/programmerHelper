
import random

from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from apps.tags.models import Tag
from apps.comments.factories import CommentFactory
from apps.marks.factories import MarkFactory

from utils.django.factories_utils import (
    generate_text_random_length_for_field_of_model,
    AbstractTimeStampedFactory,
    generate_image,
)

from .models import Article, Subsection


class SubsectionFactory(factory.DjangoModelFactory):

    class Meta:
        model = Subsection

    @factory.lazy_attribute
    def name(self):
        return generate_text_random_length_for_field_of_model(self, 'name')

    @factory.lazy_attribute
    def content(self):
        return generate_text_random_length_for_field_of_model(self, 'content')


class ArticleFactory(AbstractTimeStampedFactory):

    class Meta:
        model = Article

    status = fuzzy.FuzzyChoice([val for val, label in Article.STATUS_ARTICLE])

    @factory.lazy_attribute
    def user(self):
        return fuzzy.FuzzyChoice(get_user_model()._default_manager.all()).fuzz()

    @factory.lazy_attribute
    def name(self):
        return generate_text_random_length_for_field_of_model(self, 'name')

    @factory.lazy_attribute
    def quotation(self):
        return generate_text_random_length_for_field_of_model(self, 'quotation')

    @factory.lazy_attribute
    def heading(self):
        return generate_text_random_length_for_field_of_model(self, 'heading')

    @factory.lazy_attribute
    def conclusion(self):
        return generate_text_random_length_for_field_of_model(self, 'conclusion')

    @factory.lazy_attribute
    def image(self):
        return generate_image(filename='article.png')

    @factory.lazy_attribute
    def source(self):
        if random.random() > .5:
            site_name = factory.Faker('url', locale='ru').generate([])
            article_slug = slugify(self.name, allow_unicode=True)
            return '{0}{1}/'.format(site_name, article_slug)
        return

    @factory.lazy_attribute
    def links(self):

        links = list()
        for i in range(random.randint(1, Article.MAX_COUNT_LINKS)):
            site_host = factory.Faker('url').generate([])
            url_name = factory.Faker('slug').generate([])
            full_path = site_host + url_name
            links.append(full_path)
        return links

    @factory.post_generation
    def comments(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 10)):
            CommentFactory(content_object=self)

    @factory.post_generation
    def tags(self, created, extracted, **kwargs):
        count_tags = random.randrange(settings.MIN_COUNT_TAGS_ON_OBJECT, settings.MAX_COUNT_TAGS_ON_OBJECT)
        tags = random.sample(tuple(Tag.objects.all()), count_tags)
        self.tags.set(tags)

    @factory.post_generation
    def marks(self, created, extracted, **kwargs):
        for i in range(random.randint(0, 10)):
            MarkFactory(content_object=self)

    @factory.post_generation
    def date_added(self, created, extracted, **kwargs):
        self.date_added = fuzzy.FuzzyDateTime(self.user.date_joined).fuzz()
        self.save()

    @factory.post_generation
    def subsections(self, created, extracted, **kwargs):

        for i in range(random.randint(1, Article.MAX_COUNT_SUBSECTIONS)):
            SubsectionFactory(article=self)
