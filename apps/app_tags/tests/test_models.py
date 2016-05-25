
from django.test import TestCase

from apps.app_tags.models import Tag
from apps.app_tags.factories import factory_tags


class Test_Tag(TestCase):

    def setUp(self):
        factory_tags(1)
        self.tag = Tag.objects.get()

    def test_create_tag(self):
        count_tags = Tag.objects.count()
        tag = Tag(name='Linux-по-русски')
        tag.full_clean()
        tag.save()
        self.assertEqual(Tag.objects.count(), count_tags + 1)
        self.assertEqual(tag.name, 'Linux-по-русски')

    def test_update_tag(self):
        new_name = 'документация-jQuery'
        self.tag.name = new_name
        self.tag.save()
        self.assertEqual(self.tag.name, 'документация-jQuery')

    def test_delete_tag(self):
        count_tags = Tag.objects.count()
        self.tag.delete()
        self.assertEqual(Tag.objects.count(), count_tags - 1)
