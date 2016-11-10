
from django.core.management import call_command


def signal_post_migrate_model_levels_of_users(sender, **kwargs):
    call_command('create_levels_of_users')
    call_command('create_groups')
    call_command('create_superuser')
