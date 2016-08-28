
import uuid
import pathlib
import shutil
import random
import string

from django.conf import settings

from invoke import task

from mylabour.logging_utils import create_logger_by_filename


logger = create_logger_by_filename(__name__)


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
def git_push(ctx, text_commit):

    # made copy project to another disk
    # use difflib and replace only changed
    # make_backup_project()

    # execute pushing with Git
    ctx.run('git add -u')
    ctx.run('git add .')
    logger.debug('Added files')
    ctx.run('git commit -m \"{0}\"'.format(text_commit))
    logger.debug('Made commit')
    ctx.run('git push -u origin master')
    logger.debug('Pushed changes to GitHub')


@task
def remove_migrations_files(ctx):
    """Remove all files for migrations in own apps, placed in folder ./apps/ ."""

    # get all own apps
    own_app_path_config = (
        app_path_config for app_path_config in settings.INSTALLED_APPS
        if app_path_config.startswith('apps.')
    )

    for app_path_config in own_app_path_config:

        # get app`s name
        app_name = app_path_config.split('.')[1]
        logger.debug('App`s name is next: %s' % app_name)

        # get a full path to a folder with migration`s files
        path_to_migration_files = settings.BASE_DIR.child('apps', app_name, 'migrations')
        logger.debug('Path to migration`s folder is next: %s' % path_to_migration_files)

        # get all files and folders in the folder with migration`s files
        paths = path_to_migration_files.listdir(pattern=None, names_only=False)
        logger.debug('Path to migration`s folder contains %d objects' % len(paths))

        for path in paths:

            # we don`t need remove a file __init__.py,
            # since it pointing what the folder for migrations is package
            if not path.endswith('__init__.py'):

                # remove files and folders
                try:
                    path.rmtree()
                    logger.debug('A object %s succeful removed.' % path.components()[-1])
                except Exception as msg:
                    logger.error('Attemt remove migrations files was falled. A reasen next:')
                    logger.error(msg)

    logger.debug('All the migrations files in own apps were succeful deleted.')


@task
def recreate_db(ctx):
    """Recreating PostreSql database with recreating and applying migrations,
    and also create default superuser."""

    # a simple system`s protect
    random_symbol = random.choice(string.ascii_uppercase)
    answer_from_user = input(
        'Are you sure, what you feel like recreate database? If yes, please type "{0}": '.format(random_symbol)
    )

    # if a user is adequate or very, very, very lucky
    if answer_from_user == random_symbol:

        # clear all files for migrations
        ctx.run('invoke remove_migrations_files')
        logger.debug('Clear migrations files')

        # disable all connects for databases,
        # for it, make to restart the PostgreSQL server
        ctx.run('sudo service postgresql stop')
        ctx.run('sudo service postgresql start')
        logger.debug('Server PostgreSQL was restarted')

        # get an attributes of a using database
        user_password = settings.DATABASES['default']['PASSWORD']
        db_user = settings.DATABASES['default']['USER']
        db_name = settings.DATABASES['default']['NAME']
        logger.debug(
            'Database has next settings:\n\tNAME - {0}\n\tUSER - {1}\n\tPASSWORD - {2}\n'.format(
                db_name,
                db_user,
                user_password,
            )
        )

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
                ctx.run(full_command)
            except Exception as msg:
                logger.error('Creating new database is falled.')
                logger.debug(msg)

        # create migrations and to apply it to the newly database
        ctx.run('./manage.py makemigrations')
        logger.debug('Created migrations for database.')
        ctx.run('./manage.py migrate')
        logger.debug('Applied migrations to database.')
