
import random
import string

from django import setup
from django.apps import apps
import pathlib
import shutil

from django.contrib.auth import get_user_model
from django.conf import settings

from invoke import run, task


@task
def make_translation():
    run('./manage.py  makemesages')


@task
def git_push(text_commit):
    run('git add -u')
    run('git add .')
    run('git commit -m \"{0}\"'.format(text_commit))
    run('git push -u origin master')


@task
def rm_migrations_files():
    try:
        run('rm apps/app_*/migrations/0*.py')
        run('rm -rf apps/app_*/migrations/__pycache__')
    except:
        print('Deteting raise error')
    else:
        print("All migrations files in apps succeful deleted.")


@task
def startapp(list_apps_names_separeted_commas):
    if list_apps_names_separeted_commas:
        if ',' in list_apps_names_separeted_commas:
            apps_names = list_apps_names_separeted_commas.split(',')
        else:
            apps_names = [list_apps_names_separeted_commas]
        print('-'*80)
        print('Attentively check out next listing wished applications:')
        print('-'*80)
        for app_name in apps_names:
            app_name = 'app_' + app_name
            print(app_name)
        flag_continuation = input('If all right, please enter "yes" or 1: ')
        if flag_continuation.lower() == 'yes' or flag_continuation == '1':
            path_to_base_dir = shutil.os.path.dirname(__file__)
            path_to_folder_apps = path_to_base_dir + '/apps'
            if not shutil.os.path.isdir(path_to_folder_apps):
                pathlib.Path(path_to_folder_apps).mkdir()
            for app_name in apps_names:
                app_name = 'app_' + app_name
                path_to_app = '{0}/{1}/'.format(path_to_folder_apps, app_name)
                # creating folders
                for dirname in [
                    'migrations',
                    'templates',
                    'templates/' + app_name,
                    'static',
                    'static/' + app_name,
                    'static/' + app_name + '/js',
                    'static/' + app_name + '/css',
                    'static/' + app_name + '/img',
                ]:
                    run('mkdir -p {0}{1}'.format(path_to_app, dirname))
                # creating empty files
                for filename in [
                    '__init__.py',
                    'urls.py',
                    'views.py',
                    'models.py',
                    'forms.py',
                    'admin.py',
                    'apps.py',
                    'test_models.py',
                    'test_views.py',
                    'test_forms.py',
                    'templates/' + app_name + '/' + app_name + '_skeleton.html',
                    'static/' + app_name + '/js/' + app_name + '.js',
                    'migrations/__init__.py',
                    'static/' + app_name + '/css/' + app_name + '.css',
                ]:
                    path_to_file = '{0}/{1}/{2}'.format(path_to_folder_apps, app_name, filename)
                    pathlib.Path(path_to_file).touch()
                path_to_app = '{0}/{1}/'.format(path_to_folder_apps, app_name)
                with open(path_to_app + 'models.py', 'w') as f:
                    f.writelines('\n'.join([
                        '\nimport uuid\n',
                        'from django.core.urlresolvers import reverse',
                        'from django.core.validators import MinLengthValidator',
                        'from django.utils.translation import ugettext_lazy as _',
                        'from django.db import models',
                        'from django.conf import settings',
                        '\n\n\n',
                    ]))
                with open(path_to_app + 'urls.py', 'w') as f:
                    f.writelines('\n'.join([
                        "\nfrom django.conf.urls import url\n",
                        "\napp_name = 'app_'\n",
                        "urlpatterns = [\n    url(r'/$', .as_view(), {}, ''),\n]\n",
                    ]))
                with open(path_to_app + 'views.py', 'w') as f:
                    f.writelines('\n'.join([
                        '\nfrom django.views.generic import DetailView\n',
                    ]))
                with open(path_to_app + 'apps.py', 'w') as f:
                    f.writelines('\n'.join([
                        '\nfrom django.utils.translation import ugettext_lazy as _',
                        'from django.apps import AppConfig\n',
                        '\nclass AppConfig(AppConfig):',
                        '    name = "apps.app_"',
                        '    verbose_name = _("")\n',
                    ]))
                with open(path_to_app + 'admin.py', 'w') as f:
                    f.writelines('\n'.join([
                        '\nfrom django.db.models import Count',
                        'from django.utils.translation import ugettext_lazy as _',
                        'from django.contrib import admin\n\n',
                    ]))
                with open(path_to_app + 'forms.py', 'w') as f:
                    f.writelines('\n'.join([
                        '\nfrom django import forms\n',
                    ]))
                with open(path_to_app + 'test_models.py', 'w') as f:
                    f.writelines('\n'.join([
                        '\nimport random\n',
                        'import factory',
                        'from factory import fuzzy\n',
                        'from .models import *\n',
                    ]))
        else:
            print('-'*80)
            print('Nothing worked')
    else:
        print('Nothing worked')


@task
def recreate_db():
    """
    Recreating PostreSql database with recreating and applying migrations, and also create default superuser.
    """

    random_symbol = random.choice(string.ascii_uppercase)
    answer_from_user = input(
        'Are you sure, what you feel like recreate database? If yes, please type "{0}": '.format(random_symbol)
    )
    if answer_from_user == random_symbol:
        run('invoke rm_migrations_files')
        print('Clear migrations files')
        # disable all connects for databases
        run('sudo service postgresql stop')
        run('sudo service postgresql start')
        # getting attributes database
        user_password = settings.DATABASES['default']['PASSWORD']
        db_user = settings.DATABASES['default']['USER']
        db_name = settings.DATABASES['default']['NAME']
        # recreate database and role
        connect = 'sudo -u postgres psql -c '
        all_commands = """
        DROP DATABASE {db_name};
        DROP ROLE {db_user};
        CREATE ROLE {db_user} LOGIN PASSWORD '{user_password}' CREATEDB;
        CREATE DATABASE {db_name} WITH OWNER = {db_user}
            ENCODING = 'UTF8'
            TABLESPACE = pg_default
            LC_COLLATE = 'en_US.UTF-8'
            LC_CTYPE = 'en_US.UTF-8'
            CONNECTION LIMIT = -1;
        GRANT CONNECT, TEMPORARY ON DATABASE {db_name} TO public;
        GRANT ALL ON DATABASE {db_name} TO {db_user};
        """.format(user_password=user_password, db_user=db_user, db_name=db_name)
        for line in all_commands.split(';'):
            command = line.strip() + ';'
            try:
                full_command = '{0} "{1}"'.format(connect, command)
                run(full_command)
            except:
                pass
        # executing migrations
        run('./manage.py makemigrations')
        run('./manage.py migrate')
        # create main superuser
        # create_default_superuser()


@task
def create_default_superuser():
    # load apps in registry if not ready
    if not apps.ready:
        setup()
    # get user_model
    USER_MODEL = get_user_model()
    USER_MODEL.objects.create_superuser(
        email='setivolkylany@gmail.com',
        username='setivolkylany',
        password='lv210493',
        date_birthday='2000-12-12',
    )
    print('-'*50)
    print('Succesful added superuser!')
    print('-'*50)
