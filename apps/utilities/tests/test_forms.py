
from django.contrib import admin

from suit.widgets import AutosizedTextarea

from utils.django.test_utils import EnhancedTestCase

from apps.utilities.forms import UtilityCategoryAdminModelForm, UtilityAdminModelForm


class UtilityCategoryAdminModelFormTests(EnhancedTestCase):

    def setUp(self):

        model = UtilityCategoryAdminModelForm._meta.model

        admin_model = admin.ModelAdmin(model, self.admin_site)
        admin_model.form = UtilityCategoryAdminModelForm

        admin_form = admin_model.get_form(self.mockrequest)

        self.form = admin_form()

    def test_attributes_of_fields_of_form(self):

        self.assertEqual(self.form.fields['name'].widget.attrs['class'], 'span12')

        self.assertTrue(self.form.fields['slug'].disabled)
        self.assertEqual(self.form.fields['slug'].widget.attrs['class'], 'span12')

        self.assertIn('span12', self.form.fields['description'].widget.attrs['class'])

        self.assertIsInstance(self.form.fields['description'].widget, AutosizedTextarea)


class UtilityAdminModelFormTests(EnhancedTestCase):

    def setUp(self):

        model = UtilityAdminModelForm._meta.model

        admin_model = admin.ModelAdmin(model, self.admin_site)
        admin_model.form = UtilityAdminModelForm

        admin_form = admin_model.get_form(self.mockrequest)

        self.form = admin_form()

    def test_attributes_of_fields_of_form(self):

        self.assertEqual(self.form.fields['name'].widget.attrs['class'], 'span12')

        self.assertEqual(self.form.fields['category'].widget.widget.attrs['class'], 'span11')

        self.assertIn('span12', self.form.fields['description'].widget.attrs['class'])

        self.assertIsInstance(self.form.fields['description'].widget, AutosizedTextarea)

        self.assertEqual(self.form.fields['web_link'].widget.attrs['class'], 'span12')
