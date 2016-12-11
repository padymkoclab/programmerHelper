
import warnings
import sys
import inspect
import fnmatch
import os
import webbrowser
import collections
import logging
import pathlib
import shutil
import random
import string

from django.conf import settings

import pip
from invoke import task


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logFormatter = logging.Formatter('%(levelname)s: %(message)s')
logHandler = logging.StreamHandler()
logHandler.setFormatter(logFormatter)
logHandler.setLevel(logging.DEBUG)
logger.addHandler(logHandler)


# width of console
TERMINAL_SIZE = shutil.get_terminal_size().columns


def checkup_path(path):

    path = pathlib.Path(path)
    if not path.exists():
        raise OSError('Path {} does not exists'.format(path.absolute()))


@task
def git_push(ctx, text_commit):
    """Prepare and commit changes to repository."""

    # made copy project to another disk
    # use difflib and replace only changed
    # make_backup_project()

    # execute pushing with Git
    ctx.run('git add -u')
    ctx.run('git add .')
    logger.debug('Added files to Git repository')
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


@task
def replace_text_in_python_files(ctx, path, original_text, replaceable_text):
    """Replace text by pattern in pythonic files."""

    def prepare_line_to_display(line, text_for_wrap, escape_code):
        """Auxilary function for wrap line to colored line by passed parameters."""

        wrapped_text = '\x1b[{}m{}\x1b[0m'.format(escape_code, text_for_wrap)
        return line.replace('\n', '').strip(' ').replace(text_for_wrap, wrapped_text)

    # check if is real path passed
    checkup_path(path)

    # if user typed same values
    if original_text == replaceable_text:
        logger.warn('Original text is equal to replaceable text.')
        return

    # var for storage files where will be found needed text
    needed_files = list()

    # find only python files
    path = pathlib.Path(path)
    for obj in path.rglob('*.py'):

        # another one restrict for files
        if not obj.is_file():
            continue

        # open file for read and write
        f = obj.open('r+')

        # var for all details of lines this file
        lines_details = dict()

        # counter founed matches
        count_found = 0

        for line_num, original_line in enumerate(f.readlines(), 1):

            # if found match in a line
            if original_text in original_line:

                # highlight original text in original line
                original_line_display = prepare_line_to_display(original_line, original_text, '3;30;41')

                # highlight replaceable text in line with corresponding replace
                replaceable_line = original_line.replace(original_text, replaceable_text)
                replaceable_line_display = prepare_line_to_display(replaceable_line, replaceable_text, '3;30;43')

                # updated counter by count founed matches in the line
                count_found += original_line.count(original_text)

            else:

                # if nothind found - all details is none
                replaceable_line = original_line_display = replaceable_line_display = None

            lines_details[line_num] = dict(
                original_line=original_line,
                replaceable_line=replaceable_line,
                original_line_display=original_line_display,
                replaceable_line_display=replaceable_line_display,
            )

        # if file contains matches
        if count_found > 0:

            # print path to file and count founded matches
            print('\x1b[1;33;44m {} (found {}) \x1b[0m'.format(f.name, count_found))
            print('-' * TERMINAL_SIZE)

            replaceable_content = str()
            original_content = str()

            for line_num, line_details in lines_details.items():

                replaceable_line = line_details['replaceable_line']
                original_line = line_details['original_line']

                # restore original content of the file a line by line
                original_content += original_line

                # made content of the file with corresponding replications, if need
                if replaceable_line is None:
                    replaceable_content += original_line
                    continue
                else:
                    replaceable_content += replaceable_line

                # print corresponding details of line
                print('{line_num:>10} | {original_line_display:<70} {replaceable_line_display}'.format(
                    line_num=line_num,
                    original_line_display=line_details['original_line_display'],
                    replaceable_line_display=line_details['replaceable_line_display'],
                ))

            # keep file as opened with an original and replacable content
            needed_files.append((f, original_content, replaceable_content))

        else:

            # close a file, if it not contains matches at all
            f.close()

    # if no one file constins matches
    if not needed_files:
        logger.info('Nothing found for matching in all files')
        return

    # display promt to a user
    user_promt = None
    try:
        while user_promt not in ['y', 'n']:
            user_promt = input('Are you agree? (Yes(y)/No(n)) ')

        if user_promt == 'n':
            logger.info('Nothing changed.')
            return
        elif user_promt == 'y':

            # if the user confimed changes
            for f, original_content, replaceable_content in needed_files:
                f.seek(0)
                f.write(replaceable_content)

    except Exception as e:

        # if something went wrong recovery the contents of files to original state
        for f, original_content, replaceable_content in needed_files:
            f.seek(0)
            f.truncate()
            f.write(original_content)
        logger.error('Changes discarted since raised error: {}'.format(e))
    else:
        if user_promt == 'y':
            # if all good, print details about it
            logger.info('Changed files: {} '.format(len(needed_files)))
            for f, *other in needed_files:
                print('\t{}'.format(f.name))
    finally:
        # close all opened files in any case
        for f, *other in needed_files:
            f.close()


@task
def rename_files(ctx, path, pattern, rename_to):
    """Make renaming files be passed parameters."""

    checkup_path(path)

    details = list()
    counter = 0
    num_column_with = 5
    origin_column_with = TERMINAL_SIZE // 2 - num_column_with
    rename_column_with = TERMINAL_SIZE - origin_column_with - num_column_with - 10

    RenameFileDetail = collections.namedtuple(
        'RenameFileDetail',
        ('match_file', 'renamed_file', 'display_line')
    )

    for dirpath, dirnames, filenames in os.walk(path):

        if not filenames:
            continue

        for file in fnmatch.filter(filenames, pattern):
            match_file = '{}/{}'.format(dirpath, file)
            renamed_file = '{}/{}'.format(dirpath, rename_to)
            counter += 1
            display_line = '{0:>{1}} | {2:<{3}} | {4:<{5}}'.format(
                counter,
                num_column_with,
                match_file,
                origin_column_with,
                renamed_file,
                rename_column_with,
            )
            details.append(
                RenameFileDetail(
                    match_file=match_file, renamed_file=renamed_file, display_line=display_line
                )
            )

    if counter <= 1:
        logger.info('Nothing found by pattern')
        return

    print('\x1b[1;37;44mFound files: {}\x1b[0m'.format(counter))
    print('-' * TERMINAL_SIZE)
    print('{0:>{1}} | {2:^{3}} | {4:^{5}}'.format(
        '№',
        num_column_with,
        'Original name',
        origin_column_with,
        'Renamed name',
        rename_column_with,
    ))
    print('-' * TERMINAL_SIZE)
    for rename_file_detail in details:
        print(rename_file_detail.display_line)

    user_promt = None
    while user_promt not in ['y', 'n']:

        user_promt = input('Are you agree? (Yes(y)/No(n)) ')

    if user_promt == 'n':
        logger.info('Nothing changed')
        return

    for detail in details:
        os.rename(detail.match_file, detail.renamed_file)

    logger.info('Changed files: {}'.format(counter))


@task
def open_github_repository_page(ctx):
    """Open in a default browser a web page of current Git repository."""

    command_result = ctx.run('git config --get remote.origin.url')
    github_repo = command_result.stdout
    github_repo_url = github_repo.replace('git@github.com:', 'github.com/', 1).rstrip('.git')
    webbrowser.open('https://' + github_repo_url)


@task
def clean_pyc(ctx):
    """Clean files with *.pyc extension"""

    pass


@task
def install_requirements(ctx):
    """Intall requirements from file"""

    pass


@task
def migrate_db(ctx):
    """Make migration of database"""

    pass


@task
def flush_cache(ctx):
    """Flush cache"""

    pass


@task(help=dict(package_name='Package name'))
def remove_package(ctx, package_name):
    """Remove package with all dependencies."""

    installed_distributions = {package.key: package for package in pip.get_installed_distributions()}

    package_name = package_name.lower()
    package = installed_distributions.get(package_name)

    if package is None:
        warnings.warn('Package {} is not found'.format(package_name), Warning)

    packages_for_removing = set()

    def determinate_packages_dependencies(package, level):

        if level == 0:
            prefix = ''
        else:
            prefix = '{}|--> '.format('  ' * level)
        print('{}{}'.format(prefix, package.project_name))
        packages_for_removing.add(package.key)
        package = installed_distributions[package.key]
        level += 1
        for require in package.requires():
            determinate_packages_dependencies(require, level)

    determinate_packages_dependencies(package, level=0)

    if len(packages_for_removing) == 1:
        print('Package {} has not dependencies.'.format(package.project_name))
    else:
        packages_must_leave = set()
        for installed_package in installed_distributions.values():
            if installed_package.key not in packages_for_removing:
                requires = {require.key for require in installed_package.requires()}
                for package_must_leave in requires.intersection(packages_for_removing):
                    packages_must_leave.add(package_must_leave)

        packages_for_removing = packages_for_removing.difference(packages_must_leave)

        if packages_must_leave:
            print(
                '\nNext packages has other dependencies, so it wouldn`t removed: {}'.format(
                    ', '.join(packages_must_leave)
                )
            )

        print('\nPackage {} has dependencies. Also will be removed:\n{}'.format(
            package.project_name,
            ', '.join(packages_for_removing)
        ))

    is_confirmed = None
    while is_confirmed not in ('', 'y', 'n'):
        is_confirmed = input('Are you agre Yes(y)/No(n): (y)')

        if is_confirmed in ('', 'y'):
            command = 'pip uninstall --yes {}'.format(' '.join(packages_for_removing))
            ctx.run(command)


@task
def get_packages_dependencies(ctx, package_name=None):
    """Display packages dependencies."""

    installed_distributions = pip.get_installed_distributions()

    packages_required_for = collections.defaultdict(list)
    for package in installed_distributions:
        for require in package.requires():
            packages_required_for[require.key].append(package)

    if package_name is None:
        packages = installed_distributions

    else:

        package_name = package_name.lower()
        package = [package for package in installed_distributions if package.key == package_name]

        if not package:
            warnings.warn('Package {} is not found'.format(package_name), Warning)
            packages = ()
        else:
            packages = package

    for package in packages:

        package_required_for = packages_required_for[package.key]
        count_package_required_for = len(package_required_for)

        requires = package.requires()
        count_requires = len(requires)

        msg_required_for = 'package' if count_package_required_for == 1 else 'packages'
        msg_dependencies = 'dependency' if count_requires == 1 else 'dependencies'

        for required_for in package_required_for:
            print('   |--> {}'.format(required_for))

        if count_package_required_for:
            print('   |')

        print(
            '\033[0;30;42m{}\033[00m - required for {} {} and has {} {}'.format(
                package.project_name,
                count_package_required_for,
                msg_required_for,
                count_requires,
                msg_dependencies,
            )
        )

        if count_requires:
            print('   ^')

        for require in requires:
            print('   |-- {}'.format(require))
