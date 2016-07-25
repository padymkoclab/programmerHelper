
from django.core.management.base import BaseCommand

from apps.tags.constants import TAGS_NAMES
from apps.tags.factories import TagFactory
from apps.tags.models import Tag


class Command(BaseCommand):

    help = 'Create tags for all project'

    def handle(self, *args, **kwargs):

        # clear database from tags
        Tag.objects.filter().delete()

        # create tags
        for tag_name in TAGS_NAMES:
            TagFactory(name=tag_name)
