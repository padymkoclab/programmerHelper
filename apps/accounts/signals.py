
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed


@receiver(user_logged_in)
def signal_logged_in_account(sender, request, user, **kwargs):
    pass


@receiver(user_logged_out)
def signal_logged_out_account(sender, request, user, **kwargs):
    pass


@receiver(user_login_failed)
def signal_login_failed_account(sender, credentials, **kwargs):
    pass
