
from django.conf import settings
from django.core.management.base import BaseCommand

import unipath


class Command(BaseCommand):
    """
    Command for clear all migration`s files in each apps.
    Apps, supposed, placed in folder apps/ and installed third-party app - unipath.
    In settings of projects a variable BASE_DIR must be instance the unipath.Path().
    """

    help_text = 'Clear all migration`s files in each a custom application.'

    def handle(self, *args, **kwargs):
        assert hasattr(settings, 'BASE_DIR'), 'In main settings of project must be variable BASE_DIR.'
        assert type(settings.BASE_DIR) == unipath.path.Path, 'The settings.BASE_DIR must instance the unipath.path.Path'

        apps_folder = settings.BASE_DIR.child('apps')
        for app_folder in apps_folder.listdir():
            for obj in app_folder.child('migrations').listdir():
                if not obj.name == '__init__.py':
                    if obj.isfile():
                        obj.remove()
                    elif obj.isdir():
                        obj.rmtree()
