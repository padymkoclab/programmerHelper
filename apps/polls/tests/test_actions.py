
from django.core.management import call_command
from django.test import TestCase

from config.admin import AdminSite

from apps.polls.tests.test_admin import mockrequest
from apps.polls.actions import make_draft, make_opened, make_closed
from apps.polls.admin import PollAdmin
from apps.polls.models import Poll


class ActionsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('factory_test_polls', '6')

        # create polls
        cls.poll1, cls.poll2, cls.poll3, cls.poll4, cls.poll5, cls.poll6 = Poll.objects.all()

    def setUp(self):

        # changes statuses of polls

        self.poll1.status = 'opened'
        self.poll1.full_clean()
        self.poll1.save()

        self.poll2.status = 'closed'
        self.poll2.full_clean()
        self.poll2.save()

        self.poll3.status = 'opened'
        self.poll3.full_clean()
        self.poll3.save()

        self.poll4.status = 'draft'
        self.poll4.full_clean()
        self.poll4.save()

        self.poll5.status = 'opened'
        self.poll5.full_clean()
        self.poll5.save()

        self.poll6.status = 'draft'
        self.poll6.full_clean()
        self.poll6.save()

        # model admin class for polls
        self.ModelAdmin = PollAdmin(Poll, AdminSite)

    def test_action_make_opened_no_one_polls(self):
        make_opened(self.ModelAdmin, mockrequest, Poll.objects.none())

        self.poll1.refresh_from_db()
        self.poll2.refresh_from_db()
        self.poll3.refresh_from_db()
        self.poll4.refresh_from_db()
        self.poll5.refresh_from_db()
        self.poll6.refresh_from_db()

        self.assertEqual(self.poll1.status, 'opened')
        self.assertEqual(self.poll2.status, 'closed')
        self.assertEqual(self.poll3.status, 'opened')
        self.assertEqual(self.poll4.status, 'draft')
        self.assertEqual(self.poll5.status, 'opened')
        self.assertEqual(self.poll6.status, 'draft')

    def test_action_make_opened_one_poll(self):
        make_opened(self.ModelAdmin, mockrequest, Poll.objects.filter(pk=self.poll6.pk))

        self.poll1.refresh_from_db()
        self.poll2.refresh_from_db()
        self.poll3.refresh_from_db()
        self.poll4.refresh_from_db()
        self.poll5.refresh_from_db()
        self.poll6.refresh_from_db()

        self.assertEqual(self.poll1.status, 'opened')
        self.assertEqual(self.poll2.status, 'closed')
        self.assertEqual(self.poll3.status, 'opened')
        self.assertEqual(self.poll4.status, 'draft')
        self.assertEqual(self.poll5.status, 'opened')
        self.assertEqual(self.poll6.status, 'opened')

    def test_action_make_opened_all_polls(self):
        make_opened(self.ModelAdmin, mockrequest, Poll.objects.all())

        self.poll1.refresh_from_db()
        self.poll2.refresh_from_db()
        self.poll3.refresh_from_db()
        self.poll4.refresh_from_db()
        self.poll5.refresh_from_db()
        self.poll6.refresh_from_db()

        self.assertEqual(self.poll1.status, 'opened')
        self.assertEqual(self.poll2.status, 'opened')
        self.assertEqual(self.poll3.status, 'opened')
        self.assertEqual(self.poll4.status, 'opened')
        self.assertEqual(self.poll5.status, 'opened')
        self.assertEqual(self.poll6.status, 'opened')

    def test_action_make_closed_no_one_polls(self):
        make_closed(self.ModelAdmin, mockrequest, Poll.objects.none())

        self.poll1.refresh_from_db()
        self.poll2.refresh_from_db()
        self.poll3.refresh_from_db()
        self.poll4.refresh_from_db()
        self.poll5.refresh_from_db()
        self.poll6.refresh_from_db()

        self.assertEqual(self.poll1.status, 'opened')
        self.assertEqual(self.poll2.status, 'closed')
        self.assertEqual(self.poll3.status, 'opened')
        self.assertEqual(self.poll4.status, 'draft')
        self.assertEqual(self.poll5.status, 'opened')
        self.assertEqual(self.poll6.status, 'draft')

    def test_action_make_closed_one_poll(self):
        make_closed(self.ModelAdmin, mockrequest, Poll.objects.filter(pk=self.poll1.pk))

        self.poll1.refresh_from_db()
        self.poll2.refresh_from_db()
        self.poll3.refresh_from_db()
        self.poll4.refresh_from_db()
        self.poll5.refresh_from_db()
        self.poll6.refresh_from_db()

        self.assertEqual(self.poll1.status, 'closed')
        self.assertEqual(self.poll2.status, 'closed')
        self.assertEqual(self.poll3.status, 'opened')
        self.assertEqual(self.poll4.status, 'draft')
        self.assertEqual(self.poll5.status, 'opened')
        self.assertEqual(self.poll6.status, 'draft')

    def test_action_make_closed_all_polls(self):
        make_closed(self.ModelAdmin, mockrequest, Poll.objects.all())

        self.poll1.refresh_from_db()
        self.poll2.refresh_from_db()
        self.poll3.refresh_from_db()
        self.poll4.refresh_from_db()
        self.poll5.refresh_from_db()
        self.poll6.refresh_from_db()

        self.assertEqual(self.poll1.status, 'closed')
        self.assertEqual(self.poll2.status, 'closed')
        self.assertEqual(self.poll3.status, 'closed')
        self.assertEqual(self.poll4.status, 'closed')
        self.assertEqual(self.poll5.status, 'closed')
        self.assertEqual(self.poll6.status, 'closed')

    def test_action_make_draft_no_one_polls(self):
        make_draft(self.ModelAdmin, mockrequest, Poll.objects.none())

        self.poll1.refresh_from_db()
        self.poll2.refresh_from_db()
        self.poll3.refresh_from_db()
        self.poll4.refresh_from_db()
        self.poll5.refresh_from_db()
        self.poll6.refresh_from_db()

        self.assertEqual(self.poll1.status, 'opened')
        self.assertEqual(self.poll2.status, 'closed')
        self.assertEqual(self.poll3.status, 'opened')
        self.assertEqual(self.poll4.status, 'draft')
        self.assertEqual(self.poll5.status, 'opened')
        self.assertEqual(self.poll6.status, 'draft')

    def test_action_make_draft_one_poll(self):
        make_draft(self.ModelAdmin, mockrequest, Poll.objects.filter(pk=self.poll1.pk))

        self.poll1.refresh_from_db()
        self.poll2.refresh_from_db()
        self.poll3.refresh_from_db()
        self.poll4.refresh_from_db()
        self.poll5.refresh_from_db()
        self.poll6.refresh_from_db()

        self.assertEqual(self.poll1.status, 'draft')
        self.assertEqual(self.poll2.status, 'closed')
        self.assertEqual(self.poll3.status, 'opened')
        self.assertEqual(self.poll4.status, 'draft')
        self.assertEqual(self.poll5.status, 'opened')
        self.assertEqual(self.poll6.status, 'draft')

    def test_action_make_draft_all_polls(self):
        make_draft(self.ModelAdmin, mockrequest, Poll.objects.all())

        self.poll1.refresh_from_db()
        self.poll2.refresh_from_db()
        self.poll3.refresh_from_db()
        self.poll4.refresh_from_db()
        self.poll5.refresh_from_db()
        self.poll6.refresh_from_db()

        self.assertEqual(self.poll1.status, 'draft')
        self.assertEqual(self.poll2.status, 'draft')
        self.assertEqual(self.poll3.status, 'draft')
        self.assertEqual(self.poll4.status, 'draft')
        self.assertEqual(self.poll5.status, 'draft')
        self.assertEqual(self.poll6.status, 'draft')
