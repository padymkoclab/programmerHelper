
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

import psycopg2 as Database  # NOQA


class Command(BaseCommand):
    help = 'Remove exists the database for testing.'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        settings_for_DB = settings.DATABASES['default']
        name_test_database = settings.DATABASES['default']['TEST']['NAME']

        conn = dict()
        for name, value in settings_for_DB.items():
            name = name.lower()
            if name in ['password', 'name', 'user', 'host', 'port']:
                if name == 'name':
                    name = 'database'
                conn[name] = value
        del settings_for_DB

        try:
            connection = Database.connect(**conn)
            connection.set_isolation_level(0)  # autocommit false
            cursor = connection.cursor()
            drop_query = "DROP DATABASE IF EXISTS \"%s\";" % name_test_database
            logging.info('Executing: "' + drop_query + '"')
            cursor.execute(drop_query)
        except Database.ProgrammingError as e:
            raise Exception(e)
            logging.exception("Error: %s" % str(e))
        finally:
            if 'connection' in vars():
                connection.close()
