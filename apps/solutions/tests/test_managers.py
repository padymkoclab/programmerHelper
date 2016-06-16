
import unittest

from django.test import TestCase

from apps.accounts.factories import accounts_factory
from apps.tags.factories import tags_factory
from apps.badges.factories import badges_factory
from apps.web_links.factories import web_links_factory
# from apps.comments.factories import CommentFactory
# from apps.scopes.factories import ScopeFactory
# from apps.tags.models import Tag
# from apps.web_links.models import WebLink
# from mylabour.utils import generate_text_certain_length

from apps.solutions.factories import solutions_factory, SolutionFactory
# from apps.solutions.models import Solution


class SolutionManagerTest(TestCase):
    """
    Tests for manager of solutions.
    """

    @classmethod
    def setUpTestData(self):
        tags_factory(15)
        web_links_factory(15)
        badges_factory()
        accounts_factory(15)

    def setUp(self):
        solutions_factory(3)

    @unittest.skip('Not implemented')
    def test_comlain_on_the_solution(self):
        pass
