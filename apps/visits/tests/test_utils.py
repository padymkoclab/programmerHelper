
import unittest

import pytest

from ..utils import parse_user_agent_string


class UtilsTest(unittest.TestCase):

    def test_parse_user_agent_string_1(self):

        assert parse_user_agent_string(
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        ) == ('Linux', 'Chrome')

    def test_parse_user_agent_string_2(self):

        assert parse_user_agent_string(
            'Opera/9.80 (X11; Linux x86_64; Edition Linux Mint) Presto/2.12.388 Version/12.16'
        ) == ('Linux', 'Opera')

    def test_parse_user_agent_string_3(self):

        assert parse_user_agent_string(
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
        ) == ('Linux', 'Firefox')

    def test_parse_user_agent_string_4(self):

        assert parse_user_agent_string(
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'
        ) == ('Windows', 'Internet Explorer')

    def test_parse_user_agent_string_5(self):

        assert parse_user_agent_string(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
        ) == ('Windows', 'Edge')

    def test_parse_user_agent_string_6(self):

        assert parse_user_agent_string(
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
        ) == ('Macintosh', 'Safari')

    def test_parse_user_agent_string_7(self):

        assert parse_user_agent_string(
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; ja-JP) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16'
        ) == ('Windows', 'Safari')

    def test_parse_user_agent_string_8(self):

        assert parse_user_agent_string(
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
        ) == ('Windows', 'Firefox')

    def test_parse_user_agent_string_9(self):

        assert parse_user_agent_string(
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'
        ) == ('Macintosh', 'Chrome')

    def test_parse_user_agent_string_10(self):

        assert parse_user_agent_string(
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        ) == ('Windows', 'Chrome')

    def test_parse_user_agent_string_11(self):

        assert parse_user_agent_string(
            'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'
        ) == ('Windows', 'Opera')

    def test_parse_user_agent_string_12(self):

        assert parse_user_agent_string(
            'Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14'
        ) == ('Windows', 'Opera')

    def test_parse_user_agent_string_13(self):

        assert parse_user_agent_string(
            'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52'
        ) == ('Macintosh', 'Opera')

    def test_parse_user_agent_string_14(self):

        assert parse_user_agent_string(
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0'
        ) == ('Macintosh', 'Firefox')

    def test_parse_user_agent_string_15(self):

        assert parse_user_agent_string(
            'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'
        ) == ('Windows', 'Internet Explorer')
