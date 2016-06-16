
import uuid
import pathlib
import shutil
import random
import string

from django import setup
from django.apps import apps
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core import management

from invoke import run, task


@task
def make_translation():
    run('./manage.py makemesages')


def make_backup_project():
    dst = '/media/wlysenko/66ABF2AC3D03BAAA/Web/Projects/django/'
    path_to_project = pathlib.Path(__file__).parent
    project_name = path_to_project.name
    path_to_backup = dst + project_name
    try:
        shutil.copytree(str(path_to_project), path_to_backup)
    except FileExistsError:
        temp_name_project = str(uuid.uuid1())
        temp_path_to_backup = dst + temp_name_project
        try:
            shutil.copytree(str(path_to_project), temp_path_to_backup)
        except:
            raise RuntimeError('Не удалось сделать backup of project.')
        else:
            shutil.rmtree(path_to_backup)
            shutil.os.rename(temp_path_to_backup, path_to_backup)
    except:
        raise RuntimeError('Не удалось сделать backup of project.')
    else:
        return True


@task
def git_push(text_commit):

    # made copy project to another disk
    # make_backup_project()

    # execute pushing with Git
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
    print('-' * 50)
    print('Succesful added superuser!')
    print('-' * 50)


@task
def delete_testing_database():
    run('sudo service postgresql stop')
    run('sudo service postgresql start')
    # load apps in registry if not ready
    if not apps.ready:
        setup()
    management.call_command('delete_test_database')
