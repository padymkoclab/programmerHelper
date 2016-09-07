
import tempfile
import shutil

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from django.utils import timezone
from django.conf import settings, UserSettingsHolder
from django.test.signals import setting_changed
from django.test import TestCase, RequestFactory

from pyvirtualdisplay import Display
from selenium.webdriver import Chrome

from mylabour.factories_utils import generate_image
from mylabour.logging_utils import create_logger_by_filename


logger = create_logger_by_filename(__name__)
webdriver = Chrome


class EnhancedTestCase(TestCase):

    factory = RequestFactory()
    django_user_model = get_user_model()
    reverse = reverse
    timezone = timezone
    mockrequest = type('MockRequest', (), {})()
    call_command = call_command
    admin_site = admin.AdminSite()

    def __init__(self, *args, **kwargs):
        super(EnhancedTestCase, self).__init__(*args, **kwargs)
        self.reverse = reverse
        self.call_command = call_command

    @classmethod
    def setup_class(cls):
        """Override MEDIA_ROOT adn create tempdir for media while testing."""

        cls.testing_tempdir = tempfile.mkdtemp()

        cls.options = {
            'MEDIA_ROOT': cls.testing_tempdir,
            'DEFAULT_FILE_STORAGE': 'django.core.files.storage.FileSystemStorage',
        }

        override = UserSettingsHolder(settings._wrapped)
        for key, new_value in cls.options.items():
            setattr(override, key, new_value)
        cls.wrapped = settings._wrapped
        settings._wrapped = override
        for key, new_value in cls.options.items():
            setting_changed.send(sender=settings._wrapped.__class__, setting=key, value=new_value, enter=True)

        logger.debug('Create a tempdir {0} for generated assets while testing'.format(cls.testing_tempdir))

    @classmethod
    def teardown_class(cls):
        """Restore original MEDIA_ROOT adn remove tempdir for media while testing."""

        settings._wrapped = cls.wrapped
        del cls.wrapped
        for key in cls.options:
            new_value = getattr(settings, key, None)
            setting_changed.send(sender=settings._wrapped.__class__, setting=key, value=new_value, enter=False)

        shutil.rmtree(cls.testing_tempdir, ignore_errors=True)

    @classmethod
    def _make_user_as_active_superuser(cls, user):
        user.is_active = True
        user.is_superuser = True
        user.full_clean()
        user.save()

    def _logger_as_admin(self, user):
        raise NotImplementedError

    def _generate_image(self):
        return generate_image(filename='testing_image.png')


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
        admin_login_url = self.live_server_url + self.reverse('admin:login')

        # create at least one an active superuser
        self.active_superuser = self.django_user_model.objects.filter(is_active=True, is_superuser=True).first()
        username = self.active_superuser.get_username()
        password = 'admin'
        self.active_superuser.set_password(password)

        self.browser.get(admin_login_url)
        username_input = self.browser.find_element_by_xpath('//*[@id="id_username"]')
        password_input = self.browser.find_element_by_xpath('//*[@id="id_password"]')
        btn_login = self.browser.find_element_by_xpath('//*[@id="login-form"]/div[4]/input')

        username_input.send_keys(username)
        password_input.send_keys(password)
        btn_login.click()

        # Attempt make session for authorization
        #
        # simulation login superuser for get needed cookies
        # client = self.client_class()
        #
        # client.force_login(self.active_superuser)
        # cookie = client.cookies['sessionid']

        # # open the admin`s login page and add the needed cookies, and then the refresh page
        # # it is given a logger superuser in the admin
        # self.browser.get(admin_login_url)
        # self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value})
        # self.browser.refresh()

    def open_page(self, url):
        """Add host to a passed url and to open it in a browser."""

        self.browser.get(self.live_server_url + url)
