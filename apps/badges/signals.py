
from django.core.management import call_command


def create_default_badges(sender, *args, **kwargs):

    call_command('create_default_badges')
