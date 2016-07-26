
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Create groups for accounts'

    def handle(self, *args, **kwargs):
        raise NotImplementedError
