
from django.test import TestCase
from django.forms import inlineformset_factory

import pytest

from apps.polls.formsets import ChoiceInlineFormSet
from apps.polls.models import Poll, Choice
from apps.polls.forms import ChoiceModelForm
from apps.polls.factories import PollFactory, ChoiceFactory


class ChoiceInlineFormSetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.choiceinlineformset = inlineformset_factory(
            Poll,
            Choice,
            form=ChoiceModelForm,
            formset=ChoiceInlineFormSet,
            fk_name='poll',
        )
        cls.poll = PollFactory()
        cls.choice0 = ChoiceFactory(poll=cls.poll)
        cls.choice1 = ChoiceFactory(poll=cls.poll)
        cls.choice2 = ChoiceFactory(poll=cls.poll)
        cls.choice3 = ChoiceFactory(poll=cls.poll)

    def test_formset_with_diffrent_values(self):
        data = {
            'choices-TOTAL_FORMS': 3,
            'choices-INITIAL_FORMS': 0,
            'choices-0-text_choice': 'A simple text about a poll',
            'choices-1-text_choice': 'An another simple text about a poll',
            'choices-2-text_choice': 'Yet another simple text about a poll',
        }
        instance_choiceinlineformset = self.choiceinlineformset(data=data, instance=self.poll)
        self.assertTrue(instance_choiceinlineformset.is_valid())
        self.assertEqual(instance_choiceinlineformset.total_error_count(), 0)
        self.assertListEqual(instance_choiceinlineformset.errors, [{}, {}, {}])

    def test_formset_with_dublicated_values(self):
        data = {
            'choices-TOTAL_FORMS': 3,
            'choices-INITIAL_FORMS': 0,
            'choices-0-text_choice': 'A simple text about a poll',
            'choices-1-text_choice': 'An another simple text about a poll',
            'choices-2-text_choice': 'A simple text about a poll',
        }
        instance_choiceinlineformset = self.choiceinlineformset(data=data, instance=self.poll)
        self.assertFalse(instance_choiceinlineformset.is_valid())
        self.assertEqual(instance_choiceinlineformset.total_error_count(), 2)
        self.assertListEqual(
            instance_choiceinlineformset.errors,
            [
                {'text_choice': ['Poll does not have more than one choice with this text']},
                {},
                {'text_choice': ['Poll does not have more than one choice with this text']}
            ]
        )

    def test_formset_attempt_delete_1_form_while_exists_1_form(self):
        data = {
            'choices-TOTAL_FORMS': 1,
            'choices-INITIAL_FORMS': 0,
            'choices-0-text_choice': 'A simple text about a poll',
            'choices-0-DELETE': 'on',
        }
        instance_choiceinlineformset = self.choiceinlineformset(data=data, instance=self.poll)
        self.assertFalse(instance_choiceinlineformset.is_valid())
        self.assertEqual(instance_choiceinlineformset.total_error_count(), 1)
        self.assertListEqual(instance_choiceinlineformset.errors, [{}])
        self.assertListEqual(
            instance_choiceinlineformset.non_form_errors(),
            ['You try delete choices more than must be minimal number of choices in an each poll.']
        )

    def test_formset_attempt_delete_1_form_while_exists_2_forms(self):
        data = {
            'choices-TOTAL_FORMS': 2,
            'choices-INITIAL_FORMS': 0,
            'choices-0-text_choice': 'A simple text about a poll',
            'choices-1-text_choice': 'An another simple text about a poll',
            'choices-0-DELETE': 'on',
        }
        instance_choiceinlineformset = self.choiceinlineformset(data=data, instance=self.poll)
        self.assertFalse(instance_choiceinlineformset.is_valid())
        self.assertEqual(instance_choiceinlineformset.total_error_count(), 1)
        self.assertListEqual(instance_choiceinlineformset.errors, [{}, {}])
        self.assertListEqual(
            instance_choiceinlineformset.non_form_errors(),
            ['You try delete choices more than must be minimal number of choices in an each poll.']
        )

    def test_formset_attempt_delete_2_forms_while_exists_2_forms(self):
        data = {
            'choices-TOTAL_FORMS': 2,
            'choices-INITIAL_FORMS': 0,
            'choices-0-text_choice': 'A simple text about a poll',
            'choices-1-text_choice': 'An another simple text about a poll',
            'choices-0-DELETE': 'on',
            'choices-1-DELETE': 'on',
        }
        instance_choiceinlineformset = self.choiceinlineformset(data=data, instance=self.poll)
        self.assertFalse(instance_choiceinlineformset.is_valid())
        self.assertEqual(instance_choiceinlineformset.total_error_count(), 1)
        self.assertListEqual(instance_choiceinlineformset.errors, [{}, {}])
        self.assertListEqual(
            instance_choiceinlineformset.non_form_errors(),
            ['You try delete choices more than must be minimal number of choices in an each poll.']
        )
        self.assertListEqual(
            instance_choiceinlineformset._non_form_errors,
            ['You try delete choices more than must be minimal number of choices in an each poll.']
        )

    def test_formset_attempt_delete_1_form_while_exists_3_forms(self):
        data = {
            'choices-TOTAL_FORMS': 3,
            'choices-INITIAL_FORMS': 0,
            'choices-0-text_choice': 'A simple text about a poll',
            'choices-1-text_choice': 'An another simple text about a poll',
            'choices-2-text_choice': 'Yet another simple text about a poll',
            'choices-0-DELETE': 'on',
        }
        instance_choiceinlineformset = self.choiceinlineformset(data=data, instance=self.poll)
        self.assertTrue(instance_choiceinlineformset.is_valid())
        self.assertEqual(instance_choiceinlineformset.total_error_count(), 0)
        self.assertListEqual(instance_choiceinlineformset.errors, [{}, {}, {}])
        self.assertListEqual(instance_choiceinlineformset.non_form_errors(), [])

    def test_formset_attempt_delete_2_forms_while_exists_3_forms(self):
        data = {
            'choices-TOTAL_FORMS': 3,
            'choices-INITIAL_FORMS': 0,
            'choices-0-text_choice': 'A simple text about a poll',
            'choices-1-text_choice': 'An another simple text about a poll',
            'choices-2-text_choice': 'Yet another simple text about a poll',
            'choices-0-DELETE': 'on',
            'choices-1-DELETE': 'on',
        }
        instance_choiceinlineformset = self.choiceinlineformset(data=data, instance=self.poll)
        self.assertFalse(instance_choiceinlineformset.is_valid())
        self.assertEqual(instance_choiceinlineformset.total_error_count(), 1)
        self.assertListEqual(instance_choiceinlineformset.errors, [{}, {}, {}])
        self.assertListEqual(
            instance_choiceinlineformset.non_form_errors(),
            ['You try delete choices more than must be minimal number of choices in an each poll.']
        )

    def test_formset_attempt_delete_3_forms_while_exists_3_forms(self):
        data = {
            'choices-TOTAL_FORMS': 3,
            'choices-INITIAL_FORMS': 0,
            'choices-0-text_choice': 'A simple text about a poll',
            'choices-1-text_choice': 'An another simple text about a poll',
            'choices-2-text_choice': 'Yet another simple text about a poll',
            'choices-0-DELETE': 'on',
            'choices-1-DELETE': 'on',
            'choices-2-DELETE': 'on',
        }
        instance_choiceinlineformset = self.choiceinlineformset(data=data, instance=self.poll)
        self.assertFalse(instance_choiceinlineformset.is_valid())
        self.assertEqual(instance_choiceinlineformset.total_error_count(), 1)
        self.assertListEqual(instance_choiceinlineformset.errors, [{}, {}, {}])
        self.assertListEqual(
            instance_choiceinlineformset.non_form_errors(),
            ['You try delete choices more than must be minimal number of choices in an each poll.']
        )

    def test_formset_attempt_delete_2_forms_while_exists_4_forms(self):
        data = {
            'choices-TOTAL_FORMS': 4,
            'choices-INITIAL_FORMS': 0,
            'choices-0-text_choice': 'A simple text about a poll',
            'choices-1-text_choice': 'An another simple text about a poll',
            'choices-2-text_choice': 'Yet another simple text about a poll',
            'choices-3-text_choice': 'And again, yet another simple text about a poll',
            'choices-0-DELETE': 'on',
            'choices-1-DELETE': 'on',
        }
        instance_choiceinlineformset = self.choiceinlineformset(data=data, instance=self.poll)
        self.assertTrue(instance_choiceinlineformset.is_valid())
        self.assertEqual(instance_choiceinlineformset.total_error_count(), 0)
        self.assertListEqual(instance_choiceinlineformset.errors, [{}, {}, {}, {}])
        self.assertListEqual(instance_choiceinlineformset.non_form_errors(), [])

    def test_formset_attempt_delete_3_forms_while_exists_4_forms(self):
        data = {
            'choices-TOTAL_FORMS': 4,
            'choices-INITIAL_FORMS': 0,
            'choices-0-text_choice': 'A simple text about a poll',
            'choices-1-text_choice': 'An another simple text about a poll',
            'choices-2-text_choice': 'Yet another simple text about a poll',
            'choices-3-text_choice': 'And again, yet another simple text about a poll',
            'choices-0-DELETE': 'on',
            'choices-1-DELETE': 'on',
            'choices-2-DELETE': 'on',
        }
        instance_choiceinlineformset = self.choiceinlineformset(data=data, instance=self.poll)
        self.assertFalse(instance_choiceinlineformset.is_valid())
        self.assertEqual(instance_choiceinlineformset.total_error_count(), 1)
        self.assertListEqual(instance_choiceinlineformset.errors, [{}, {}, {}, {}])
        self.assertListEqual(
            instance_choiceinlineformset.non_form_errors(),
            ['You try delete choices more than must be minimal number of choices in an each poll.']
        )

    @pytest.mark.xfail(reason='Attribute deleted_forms always is empty')
    def test_formset_attempt_delete_4_forms_while_exists_4_forms(self):
        data = {
            'choices-TOTAL_FORMS': 4,
            'choices-INITIAL_FORMS': 2,
            'choices-MAX_NUM_FORMS': '',
            'choices-0-id': self.choice0.pk,
            'choices-1-id': self.choice1.pk,
            'choices-2-id': self.choice2.pk,
            'choices-3-id': self.choice3.pk,
            'choices-0-text_choice': 'A simple text about a poll',
            'choices-1-text_choice': 'An another simple text about a poll',
            'choices-2-text_choice': 'Yet another simple text about a poll',
            'choices-3-text_choice': 'And again, yet another simple text about a poll',
            'choices-0-DELETE': 'on',
            'choices-1-DELETE': 'on',
            'choices-2-DELETE': 'on',
            'choices-3-DELETE': 'on',
        }

        instance_choiceinlineformset = self.choiceinlineformset(data=data, instance=self.poll)
        self.assertFalse(instance_choiceinlineformset.is_valid())
        self.assertEqual(instance_choiceinlineformset.total_error_count(), 1)
        self.assertListEqual(instance_choiceinlineformset.errors, [{}, {}, {}, {}])
        self.assertEqual(instance_choiceinlineformset.deleted_forms, 4)
        self.assertListEqual(
            instance_choiceinlineformset.non_form_errors(),
            ['You try delete choices more than must be minimal number of choices in an each poll.']
        )
