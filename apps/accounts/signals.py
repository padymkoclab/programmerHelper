
from django.core.management import call_command
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

from mylabour.utils import create_logger_by_filename


logger = create_logger_by_filename(__name__)


@receiver(user_logged_in)
def signal_logged_in_account(sender, request, user, **kwargs):
    pass


@receiver(user_logged_out)
def signal_logged_out_account(sender, request, user, **kwargs):
    pass


@receiver(user_login_failed)
def signal_login_failed_account(sender, credentials, **kwargs):
    pass


def signal_post_migrate_model_levels_of_accounts(sender, **kwargs):
    call_command('create_levels_of_accounts')
    call_command('create_default_superuser')
    logger.debug('A signal post_migration for app Accounts was called')
