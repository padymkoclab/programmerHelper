
from django.core.urlresolvers import reverse
from django.test import TestCase

from apps.core.test import StaticLiveAdminTest
from apps.polls.forms import PollModelForm, ChoiceModelForm


class PollModelFormTest(TestCase):
    """
    Tests for modelForm of the model Poll.
    """

    @classmethod
    def setUpTestData(cls):

        cls.form = PollModelForm()

    def test_attrs_of_field_slug(self):

        field = self.form.fields['slug']
        widget = field.widget
        self.assertTrue(field.disabled)
        self.assertEqual(widget.attrs['class'], 'span12')

    def test_attrs_of_field_title(self):

        widget = self.form.fields['title'].widget
        self.assertEqual(widget.attrs['placeholder'], 'Enter a title of poll')
        self.assertEqual(widget.attrs['autocomplete'], 'off')
        self.assertEqual(widget.attrs['class'], 'span12')

    def test_attrs_of_field_status(self):

        widget = self.form.fields['status'].widget
        self.assertEqual(widget.attrs['class'], 'span12')


class PollModelFormLiveAdminTest(StaticLiveAdminTest):
    """
    Live tests for modelForm of the model Poll.
    """

    def test_display_modelform_in_admin(self):

        # open a page for add poll
        self.open_page(reverse('admin:polls_poll_add'))

        # find elements on the page
        input_title = self.browser.find_element_by_id('id_title')
        input_slug = self.browser.find_element_by_id('id_slug')
        input_status = self.browser.find_element_by_id('id_status')

        # checkup an input for title of poll
        self.assertEqual(input_title.get_attribute('placeholder'), 'Enter a title of poll')
        self.assertEqual(input_title.get_attribute('class'), 'span12')
        self.assertEqual(input_title.get_attribute('autocomplete'), 'off')

        # checkup an input for slug of poll
        self.assertEqual(input_slug.get_attribute('disabled'), 'true')
        self.assertEqual(input_slug.get_attribute('class'), 'span12')

        # checkup an input for status of poll
        self.assertEqual(input_status.get_attribute('class'), 'span12')


class ChoiceModelFormTest(TestCase):
    """
    Tests for modelForm of the model Choice.
    """

    @classmethod
    def setUpTestData(cls):

        cls.form = ChoiceModelForm()

    def test_attrs_of_field_text_choice(self):

        widget = self.form.fields['text_choice'].widget
        self.assertEqual(widget.attrs['class'], 'span11')
        self.assertEqual(widget.attrs['placeholder'], 'Enter text of a choice')
        self.assertEqual(widget.attrs['row'], 5)

    def test_attrs_of_field_poll(self):

        # since it is FK, this widget is relatedFieldWidgetWrapper
        widget = self.form.fields['poll'].widget.widget
        self.assertEqual(widget.attrs['class'], 'span11')


class ChoiceModelFormLiveAdminTest(StaticLiveAdminTest):
    """
    Live tests for modelForm of the model Poll.
    """

    def test_display_modelform_in_admin(self):

        # open a page for add choice
        self.open_page(reverse('admin:polls_choice_add'))

        # find elements on the page
        input_text_choice = self.browser.find_element_by_id('id_text_choice')
        input_poll = self.browser.find_element_by_id('id_poll')

        # checkup an input for text of choice
        self.assertEqual(input_text_choice.get_attribute('placeholder'), 'Enter text of a choice')
        self.assertEqual(input_text_choice.get_attribute('class'), 'span11')
        self.assertEqual(input_text_choice.get_attribute('rows'), '5')

        # checkup an input for poll of poll
        self.assertEqual(input_poll.get_attribute('class'), 'span11')
