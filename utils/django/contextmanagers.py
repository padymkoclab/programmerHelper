
import time
import contextlib

from django.db import connection

from .utils import create_logger_by_filename


logger = create_logger_by_filename(__name__)


class TimeProcessing(contextlib.ContextDecorator):
    """ """

    def __enter__(self):

        # keep time start of a process
        self.start_time = time.time()

        return self

    def __exit__(self, *args):

        # get a time after the process
        end_time = time.time()

        # determinate a time of pocessing in seconds
        seconds = end_time - self.start_time

        # make log
        logger.debug('Time processing: {0:.3} seconds'.format(seconds))


class CountSQLQueries(contextlib.ContextDecorator):
    """ """

    def __enter__(self):

        self.count_queries_before = len(connection.queries)
        return self

    def __exit__(self, *args):
        count_queries_after = len(connection.queries)
        count_queries = count_queries_after - self.count_queries_before
        logger.debug('Count queries: {0}'.format(count_queries))
