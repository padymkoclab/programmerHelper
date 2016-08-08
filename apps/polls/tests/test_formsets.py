
from django.test import TestCase
from django.forms import inlineformset_factory

from apps.polls.formsets import ChoiceInlineFormSet
from apps.polls.models import Poll, Choice
from apps.polls.forms import ChoiceModelForm


class ChoiceInlineFormSetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        self.inlineformset = inlineformset_factory(Poll, Choice, form=ChoiceModelForm, formset=ChoiceInlineFormSet)

    def setUp(self):
        pass

    def test_(self):
        data = {
            '': '',
        }
