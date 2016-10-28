
from django.core.management import call_command


def create_tags_if_yet_not(sender, **kwargs):

    call_command('create_tags')
