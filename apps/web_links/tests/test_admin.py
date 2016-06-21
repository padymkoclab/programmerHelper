
import unittest

from django.test import TestCase

from apps.web_links.factories import web_links_factory

from apps.web_links.factories import WebLinkFactory
from apps.web_links.models import WebLink
from mylabour.utils import has_connect_to_internet


class WebLinkAdminTest(TestCase):
    """
    Tests for model of web links.
    """

    @classmethod
    def setUpTestData(cls):
        web_links_factory(20)

    @unittest.skip('Error')
    def test_presence_field_status_in_each_weblink(self):
        raise NotImplementedError
