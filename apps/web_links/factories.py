
import factory

from .models import *


class WebLinkFactory(factory.DjangoModelFactory):

    class Meta:
        model = WebLink

    @factory.lazy_attribute
    def url(self):
        url = factory.Faker('url', locale='en').generate([])
        slug_url = factory.Faker('slug').generate([])
        return url + slug_url

    @factory.lazy_attribute
    def title(self):
        name_ru = factory.Faker('text', locale='ru').generate([])[:25]
        name_en = factory.Faker('text', locale='en').generate([])[:25]
        return '{0} {1}'.format(name_en, name_ru)


def web_links_factory(count):
    WebLink.objects.filter().delete()
    for i in range(count):
        WebLinkFactory()
