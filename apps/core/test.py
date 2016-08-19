
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from pyvirtualdisplay import Display
from selenium.webdriver import Chrome

webdriver = Chrome


class StaticLiveTest(StaticLiveServerTestCase):
    """
    Own StaticLiveServerTestCase with additional variables built-in in class.
    """

    reverse = reverse
    user_model = get_user_model()


class StaticLiveAdminTest(StaticLiveServerTestCase):
    """
    Live tests for modelForm of the model Poll.
    """

    @classmethod
    def setUpClass(cls):
        super(StaticLiveAdminTest, cls).setUpClass()

        User = get_user_model()
        cls.superuser = User.objects.latest()

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
        client.force_login(self.superuser)
        cookie = client.cookies['sessionid']

        # open the admin`s login page and add the needed cookies, and then the refresh page
        # it is given a logger superuser in the admin
        self.browser.get(admin_login_url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value})
        self.browser.refresh()

    def open_page(self, url):
        """Add host to a passed url and to open it in a browser."""

        self.browser.get(self.live_server_url + url)
