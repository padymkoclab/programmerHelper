
import json
import argparse

import psycopg2


parser = argparse.ArgumentParser(description="Parse command line arguments")
parser.add_argument(
    '--show_results',
    action='store_true',
    default=False,
    help='Show main data in database',
)
parser.add_argument(
    '--try_connect',
    action='store_true',
    default=False,
    help='Try connect to database',
)
parser.add_argument(
    '--update_db',
    action='store_true',
    default=False,
    help='Update a structure of database to latest',
)


def main():
    """ """

    args = parser.parse_args()

    UPDATE_DB = args.update_db
    SHOW_RESULTS = args.show_results
    TRY_CONNECT = args.try_connect

    try:
        with open('./secrets.json') as f:
            DATABASE_CONFIG = json.load(f)

        connection = psycopg2.connect(**DATABASE_CONFIG)
    except Exception as e:

        if TRY_CONNECT is True:
            print('Connect to a database is rejected: ', e)
            return

        raise
    else:

        if TRY_CONNECT is True:
            print('Succeful connected to a database')
            return

        try:

            cursor = connection.cursor()

            if SHOW_RESULTS is True:

                select_sql = """
                    SELECT
                        "users_user"."username", "users_work"."name", "users_user"."level_name"
                    FROM "project"."users_work"
                    JOIN "project"."users_user" USING (public_user_id, private_user_id);
                """

                cursor.execute(select_sql)

                table_line = '-' * 41
                print(table_line)

                print('|    Name    |    Work    |    Level    |')

                print(table_line)

                row = True
                while row is not None:
                    row = cursor.fetchone()

                    if row is not None:
                        print('|{0:^12}|{1:^12}|{2:^13}|'.format(*row))
                        print(table_line)

            if UPDATE_DB is True:

                file_sql_code = open('./code.sql', 'r')
                sql_code = file_sql_code.read()

                cursor.execute(sql_code)

            connection.commit()

        finally:

            if UPDATE_DB is True:

                file_sql_code.close()

            connection.close()


if __name__ == '__main__':
    main()
