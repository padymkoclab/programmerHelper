
import collections
import gc
import inspect

from django.dispatch import Signal
from django.core.management import BaseCommand
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import (
    pre_save, post_save, m2m_changed, pre_delete,
    post_delete, post_migrate, pre_migrate
)


SIGNAL_NAMES = {
    pre_save: 'pre_save',
    post_save: 'post_save',
    m2m_changed: 'm2m_changed',
    pre_delete: 'pre_delete',
    post_delete: 'post_delete',
    post_migrate: 'post_migrate',
    pre_migrate: 'pre_migrate',
    user_logged_in: 'user_logged_in',
    user_logged_out: 'user_logged_out',
    user_login_failed: 'user_login_failed',
}


class Command(BaseCommand):
    """

    """

    def handle(self, *args, **kwargs):

        signals = [obj for obj in gc.get_objects() if isinstance(obj, Signal)]

        signal_details = collections.defaultdict(list)

        for signal in signals:
            signal_name = SIGNAL_NAMES.get(signal, 'unknown')
            for something, weakref_ in signal.receivers:
                listener = weakref_()
                listener_name = listener.__name__
                sourcefile = inspect.getsourcefile(listener)

                signal_details[signal_name].append((listener_name, sourcefile))

        for signal_name, signal_details in signal_details.items():

            print(signal_name)
            for listener_name, fullpath in signal_details:
                print('\t{} ---> {}'.format(listener_name, fullpath))
