
# from django.dispatch import receiver, Signal, dispatcher
from django.core.management import call_command


def create_default_badges(sender, *args, **kwargs):

    call_command('create_default_badges')


# user_lost_badge = Signal(providing_args=['user', 'badge'])

# user_earned_badge = Signal(providing_args=['user', 'badge'])


# def notify_user_lost_badge()
