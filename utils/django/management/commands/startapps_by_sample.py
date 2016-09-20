
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from unipath import Path


logger = logging.getLogger('django.development')


class Command(BaseCommand):
    help = 'Create new django-app from sample template.'

    def add_arguments(self, parser):
        parser.add_argument('app_names_plural', nargs='+', type=str)

    def handle(self, *args, **options):

        app_names_plural = options['app_names_plural']

        #
        apps_dir = settings.BASE_DIR.child('apps')
        if not apps_dir.exists():
            apps_dir.mkdir()
        #
        for app_name_plural in app_names_plural:
            app_name = '{0}'.format(app_name_plural)
            app_dir = apps_dir.child(app_name)
            if app_dir.exists():
                logger.warning('App with name "%s" already exists.' % app_name)
                raise ValueError('Conflict name of app: "%s"' % app_name)

            logger.info('Start creating new app "%s" ...' % app_name)
            # create tree of directories
            Path(app_dir, 'migrations').mkdir(parents=True)
            Path(app_dir, 'migrations', '__init__.py').write_file('')
            Path(app_dir, 'management', app_name, 'commands').mkdir(parents=True)
            Path(app_dir, 'management', '__init__.py').write_file('')
            Path(app_dir, 'management', app_name, 'commands', '__init__.py').write_file('')
            Path(app_dir, 'tests').mkdir(parents=True)
            Path(app_dir, 'locale').mkdir(parents=True)
            Path(app_dir, 'static', app_name, 'img').mkdir(parents=True)

            dir_for_css = Path(app_dir, 'static', app_name, 'css')
            dir_for_css.mkdir(parents=True)
            dir_for_js = Path(app_dir, 'static', app_name, 'js')
            dir_for_js.mkdir(parents=True)
            dir_for_templates = Path(app_dir, 'templates', app_name)
            dir_for_templates.mkdir(parents=True)
            dir_for_tests = Path(app_dir, 'tests')
            dir_for_tests.mkdir(parents=True)
            logger.info('Created tree of directories!')
            # create template`s files
            dir_for_templates.child('base.html').write_file('\n{% extends "index.html" %}\n')
            dir_for_templates.child('detail.html').write_file('\n{% extends "' + app_name + '/base.html" %}\n')
            dir_for_templates.child('list.html').write_file('\n{% extends "' + app_name + '/base.html" %}\n')
            logger.info('Created template`s files!')
            # create tests files
            dir_for_tests.child('test_models.py').write_file("""
from django.test import TestCase

from apps.%s.models import *
""" % app_name)
            dir_for_tests.child('test_views.py').write_file("""
from django.test import TestCase

from apps.%s.views import *
""" % app_name)
            dir_for_tests.child('test_forms.py').write_file("""
from django.test import TestCase

from apps.%s.forms import *
""" % app_name)
            dir_for_tests.child('test_managers.py').write_file("""
from django.test import TestCase

from apps.%s.managers import *
""" % app_name)
            dir_for_tests.child('test_querysets.py').write_file("""
from django.test import TestCase

from apps.%s.querysets import *
""" % app_name)
            logger.info('Created test`s files!')
            # create static files
            dir_for_css.child(app_name + '.css').write_file("")
            dir_for_js.child(app_name + '.js').write_file("""$(function() {

});""")
            logger.info('Created static files!')
            # create working files
            app_dir.child('__init__.py').write_file('')
            app_dir.child('signals.py').write_file("""
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, m2m_changed, pre_delete, post_delete
""")
            app_dir.child('managers.py').write_file("""
from django.db import models
""")
            app_dir.child('querysets.py').write_file("""
from django.db import models
""")
            app_dir.child('models.py').write_file("""
import uuid

from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
""")
            app_dir.child('views.py').write_file("""
from django.views.generic import DetailView, ListView
""")
            app_dir.child('forms.py').write_file("""
from django import forms
""")
            app_dir.child('urls.py').write_file("""
from django.conf.urls import url

app_name = '%s'

urlpatterns = [
    #  url(r'/$', '.as_view()', {}, ''),
]
""" % app_name)
            app_dir.child('apps.py').write_file("""
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class %sConfig(AppConfig):
    name = "apps.%s"
    verbose_name = _("%s")

    def ready(self):
        pass
""" % (
                app_name.title().replace('_', ''),
                app_name,
                app_name.title().replace('_', ' ')
            )
            )
            app_dir.child('factories.py').write_file("""
import factory
from factory import fuzzy

""")
            app_dir.child('admin.py').write_file("""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
""")
            logger.info('Created working files!')
            logger.info('Successful finished creating app "%s"!' % app_name)
