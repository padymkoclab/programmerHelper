
import tempfile
import shutil

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from django.utils import timezone
from django.conf import settings
from django.test import TestCase, RequestFactory

from pyvirtualdisplay import Display
from selenium.webdriver import Chrome


webdriver = Chrome


class MockRequest:
    pass


class EnhancedTestCase(TestCase):

    factory = RequestFactory()
    django_user_model = get_user_model()
    reverse = reverse
    timezone = timezone
    settings = settings
    mockrequest = MockRequest()
    call_command = call_command

    def __init__(self, *args, **kwargs):
        super(EnhancedTestCase, self).__init__(*args, **kwargs)
        self.reverse = reverse
        self.call_command = call_command

    def setUp(self):

        self._original_MEDIA_ROOT = self.settings.MEDIA_ROOT
        self._original_DEFAULT_FILE_STORAGE = self.settings.DEFAULT_FILE_STORAGE

        self._testing_tempdir = tempfile.mkdtemp()
        self.settings.MEDIA_ROOT = self._testing_tempdir
        self.settings.DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

    def tearDown(self):

        shutil.rmtree(self._testing_tempdir, ignore_errors=True)

        self.settings.MEDIA_ROOT = self._original_MEDIA_ROOT
        self.settings.DEFAULT_FILE_STORAGE = self._original_DEFAULT_FILE_STORAGE

        del self._testing_tempdir
        del self._original_MEDIA_ROOT
        del self._original_DEFAULT_FILE_STORAGE

    @classmethod
    def _make_user_as_active_superuser(cls, user):
        user.is_active = True
        user.is_superuser = True
        user.full_clean()
        user.save()

    def _logger_as_admin(self, user):
        raise NotImplementedError


class StaticLiveAdminTest(StaticLiveServerTestCase):
    """
    Live tests for modelForm of the model Poll.
    """

    factory = RequestFactory()
    django_user_model = get_user_model()
    reverse = reverse
    timezone = timezone
    settings = settings
    call_command = call_command

    def __init__(self, *args, **kwargs):
        super(StaticLiveAdminTest, self).__init__(*args, **kwargs)
        self.reverse = reverse
        self.call_command = call_command

    @classmethod
    def setUpClass(cls):
        super(StaticLiveAdminTest, cls).setUpClass()

        # cls.call_command('factory_test_superusers', '1')
        # cls.active_superuser = cls.django_user_model.objects.get()

    def setUp(self):

        # create and start an invisible web-server
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()

        # create a browser
        self.browser = webdriver()
        self.browser.implicitly_wait(5)

        # made login in a admin as a superuser
        self.made_login_in_admin()

    def tearDown(self):

        # close the browser
        self.browser.quit()

        # close the invisible web-server
        self.display.stop()

    def made_login_in_admin(self):

        # get url for the admin`s login page
        admin_login_url = self.live_server_url + reverse('admin:login')

        # simulation login superuser for get needed cookies
        client = self.client_class()

        self.call_command('factory_test_superusers', '1')
        self.active_superuser = self.django_user_model.objects.get()

        client.force_login(self.active_superuser)
        cookie = client.cookies['sessionid']

        # open the admin`s login page and add the needed cookies, and then the refresh page
        # it is given a logger superuser in the admin
        self.browser.get(admin_login_url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value})
        self.browser.refresh()

    def open_page(self, url):
        """Add host to a passed url and to open it in a browser."""

        self.browser.get(self.live_server_url + url)
