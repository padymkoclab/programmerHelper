
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory


class EnhancedTestCase(TestCase):

    factory = RequestFactory()
    django_user_model = get_user_model()
    reverse = reverse
    timezone = timezone
    settings = settings
    liveserver = 1

    @classmethod
    def _make_user_as_active_superuser(cls, user):
        user.is_active = True
        user.is_superuser = True
        user.full_clean()
        user.save()

    def _logger_as_admin(self, user):
        raise NotImplementedError
