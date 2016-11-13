
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
