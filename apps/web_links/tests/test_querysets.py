
import unittest

from django.test import TestCase

from mylabour.utils import has_connect_to_internet

from apps.web_links.factories import WebLinkFactory
from apps.web_links.models import WebLink


class WebLinkQuerySetTest(TestCase):
    """
    Tests for queryset of a model WebLink.
    """

    @classmethod
    def setUpTestData(cls):
        cls.weblink1 = WebLinkFactory(url='https://www.youtube.com/watch?v=vy7rWy2u_m0&noredirect=1')
        cls.weblink2 = WebLinkFactory(url='https://www.youtube.com/channel/ucwtd5zjbsqgjn75mwbykynw/videos')
        cls.weblink3 = WebLinkFactory(url='https://www.google.com/')
        cls.weblink4 = WebLinkFactory(url='http://blogger.sapronov.me/2015/01/youtube.html')
        cls.weblink5 = WebLinkFactory(url='http://blogger.sapronov.me/2015/01/twitter-rss.html')
        cls.weblink6 = WebLinkFactory(url='http://www.copyblogger.com/grammar-writing-mistakes/')
        cls.weblink7 = WebLinkFactory(url='https://www.yandex.com/')
        cls.weblink8 = WebLinkFactory(url='https://www.youtube.com/watch?v=TdtrO-pxN2w')
        cls.weblink9 = WebLinkFactory(url='http://nanvel.name/2014/03/yt-thumbnails-instead-video')
        cls.weblink10 = WebLinkFactory(url='https://www.youtube.com/')
        cls.weblink11 = WebLinkFactory(url='http://www.yandex.com/does-not-exists-page/bla-bla-bla')
        cls.weblink12 = WebLinkFactory(url='http://www.dailywritingtips.com/34-writing-tips-that-will-make-you-a-better-writer/')
        cls.weblink13 = WebLinkFactory(url='http://www.youtube.com/does-not-exists-page/bla-bla-bla')
        cls.weblink14 = WebLinkFactory(url='http://www.copyblogger.com/grammar-writing-mistakes/')
        cls.weblink15 = WebLinkFactory(url='http://www.google.com/does-not-exists-page/bla-bla-bla')

    def test_random_weblinks(self):
        weblinks = WebLink.objects.all()
        # if single
        self.assertIsInstance(WebLink.objects.random_weblinks(1), WebLink)
        self.assertIn(WebLink.objects.random_weblinks(1), weblinks)
        # if several
        self.assertIsInstance(WebLink.objects.random_weblinks(2), WebLink.objects._queryset_class)
        for weblink in WebLink.objects.random_weblinks(2):
            self.assertIn(weblink, weblinks)
        self.assertIsInstance(WebLink.objects.random_weblinks(5), WebLink.objects._queryset_class)
        for weblink in WebLink.objects.random_weblinks(5):
            self.assertIn(weblink, weblinks)
        # if more than exists
        self.assertIsInstance(WebLink.objects.random_weblinks(8), WebLink.objects._queryset_class)
        for weblink in WebLink.objects.random_weblinks(8):
            self.assertIn(weblink, weblinks)

    @unittest.skipIf(not has_connect_to_internet(), 'Problem with connect to internet.')
    def test_weblinks_with_status_if_have_internet(self):
        weblinks_with_status = WebLink.objects.weblinks_with_status()
        self.assertNotIn(weblinks_with_status.get(pk=self.weblink3).is_active, True)
        self.assertNotIn(weblinks_with_status.get(pk=self.weblink7).is_active, True)
        self.assertNotIn(weblinks_with_status.get(pk=self.weblink10).is_active, True)
        self.assertNotIn(weblinks_with_status.get(pk=self.weblink11).is_active, False)
        self.assertNotIn(weblinks_with_status.get(pk=self.weblink13).is_active, False)
        self.assertNotIn(weblinks_with_status.get(pk=self.weblink15).is_active, False)

    @unittest.skipIf(has_connect_to_internet(), 'Test executed because have not internet.')
    def test_weblinks_with_status_if_have_not_internet(self):
        weblinks_with_status = WebLink.objects.weblinks_with_status()
        for weblink in WebLink.objects.weblinks_with_status():
            self.assertIsNone(weblinks_with_status.get(pk=weblink.pk).is_active)

    @unittest.skipIf(not has_connect_to_internet(), 'Problem with connect to internet.')
    def test_broken_weblinks_if_have_internet(self):
        broken_weblinks = WebLink.objects.broken_weblinks()
        self.assertNotIn(self.weblink3, broken_weblinks)
        self.assertNotIn(self.weblink7, broken_weblinks)
        self.assertNotIn(self.weblink10, broken_weblinks)
        self.assertIn(self.weblink11, broken_weblinks)
        self.assertIn(self.weblink13, broken_weblinks)
        self.assertIn(self.weblink15, broken_weblinks)

    @unittest.skipIf(has_connect_to_internet(), 'Test executed because found problems with connect to internet.')
    def test_broken_weblinks_if_have_not_internet(self):
        self.assertWarns(Warning, WebLink.objects.broken_weblinks)
        self.assertEqual(WebLink.objects.broken_weblinks().count(), 0)

    def test_weblinks_from_youtube(self):
        self.assertCountEqual(
            WebLink.objects.weblinks_from_youtube(),
            [self.weblink1, self.weblink2, self.weblink8, self.weblink10, self.weblink13]
        )
