
from django.test import TestCase

from apps.polls.factories import PollFactory, ChoiceFactory
from apps.polls.models import Poll, VoteInPoll


class PollQuerySetTest(TestCase):
    """
    Tests for queryset of polls.
    """

    @classmethod
    def setUpTestData(self):
        self.poll1 = PollFactory(status=Poll.CHOICES_STATUS.closed)
        self.poll2 = PollFactory(status=Poll.CHOICES_STATUS.opened)
        self.poll3 = PollFactory(status=Poll.CHOICES_STATUS.draft)
        self.poll4 = PollFactory(status=Poll.CHOICES_STATUS.opened)
        self.poll5 = PollFactory(status=Poll.CHOICES_STATUS.closed)
        self.poll6 = PollFactory(status=Poll.CHOICES_STATUS.draft)
        self.poll7 = PollFactory(status=Poll.CHOICES_STATUS.opened)
        self.poll8 = PollFactory(status=Poll.CHOICES_STATUS.closed)
        self.poll9 = PollFactory(status=Poll.CHOICES_STATUS.closed)
        #
        choice11 = ChoiceFactory(poll=self.poll1)
        choice12 = ChoiceFactory(poll=self.poll1)
        choice13 = ChoiceFactory(poll=self.poll1)
        choice21 = ChoiceFactory(poll=self.poll2)
        choice22 = ChoiceFactory(poll=self.poll2)
        choice23 = ChoiceFactory(poll=self.poll2)
        choice24 = ChoiceFactory(poll=self.poll2)
        choice31 = ChoiceFactory(poll=self.poll3)
        choice32 = ChoiceFactory(poll=self.poll3)
        choice33 = ChoiceFactory(poll=self.poll3)
        choice41 = ChoiceFactory(poll=self.poll4)
        choice42 = ChoiceFactory(poll=self.poll4)
        choice51 = ChoiceFactory(poll=self.poll5)
        choice52 = ChoiceFactory(poll=self.poll5)
        choice53 = ChoiceFactory(poll=self.poll5)
        choice61 = ChoiceFactory(poll=self.poll6)
        choice62 = ChoiceFactory(poll=self.poll6)
        choice63 = ChoiceFactory(poll=self.poll6)
        choice71 = ChoiceFactory(poll=self.poll7)
        choice72 = ChoiceFactory(poll=self.poll7)
        choice73 = ChoiceFactory(poll=self.poll7)
        choice81 = ChoiceFactory(poll=self.poll8)
        choice82 = ChoiceFactory(poll=self.poll8)
        choice91 = ChoiceFactory(poll=self.poll9)
        choice92 = ChoiceFactory(poll=self.poll9)
        #
        # VoteInPoll(poll=self.poll1, choi)


    def setUp(self):
        pass

    def test_closed_polls(self):
        self.assertCountEqual(
            Poll.objects.closed_polls(),
            [self.poll1, self.poll5, self.poll8, self.poll9]
        )

    def test_opened_polls(self):
        self.assertCountEqual(
            Poll.objects.opened_polls(),
            [self.poll2, self.poll4, self.poll7]
        )

    def test_draft_polls(self):
        self.assertCountEqual(Poll.objects.draft_polls(), [self.poll3, self.poll6])
