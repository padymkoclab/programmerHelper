
from django.contrib.contenttypes.models import ContentType

from mylabour.test_utils import StaticLiveAdminTest

from apps.utilities.factories import UtilityCategoryFactory, UtilityFactory
from apps.utilities.models import UtilityCategory


class UtilityCategoryAdminTest(StaticLiveAdminTest):

    @classmethod
    def setUpClass(cls):

        super().setUpClass()

        cls.call_command('factory_test_users', '10')

        cls.url_changelist = cls.reverse('admin:utilities_utilitycategory_changelist')
        cls.url_import = cls.reverse('export_import_models:import')

        cls.model = UtilityCategoryFactory._meta.model

    def test_changelist_page_presents_three_buttons(self):

        self.open_page(self.url_changelist)

        buttons = self.browser.find_elements_by_xpath('//*[@id="changelist"]/div/div[1]/a')

        # 3 buttons: Export, Import, Add
        self.assertEqual(buttons[0].text, ' Export')
        self.assertEqual(buttons[1].text, ' Import')
        self.assertEqual(len(buttons), 3)

    def test_changelist_page_link_button_import_and_export_if_no_objects(self):

        self.open_page(self.url_changelist)

        buttons = self.browser.find_elements_by_xpath('//*[@id="changelist"]/div/div[1]/a')

        # link on this page, because not objects for export
        self.assertEqual(
            buttons[0].get_attribute('href'),
            self.live_server_url + self.url_changelist + '#'
        )

        # link for import objects
        self.assertEqual(
            buttons[1].get_attribute('href'),
            self.live_server_url + self.url_import
        )

        # click on button "Export" and page simple refresh
        buttons[0].click()
        self.assertTrue(self.browser.current_url.endswith('/#'.format(self.url_changelist)))

        # click on button "Import" and move to page for import
        buttons[1].click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.url_import)

    def test_changelist_page_link_button_import_and_export_if_exist_object(self):

        category = UtilityCategoryFactory()

        self.open_page(self.url_changelist)

        buttons = self.browser.find_elements_by_xpath('//*[@id="changelist"]/div/div[1]/a')

        # a button "Export"
        export_url = self.reverse(
            'export_import_models:export',
            kwargs={
                'contenttype_model_pk': ContentType.objects.get_for_model(self.model).pk,
                'pks_separated_commas': category.pk
            }
        )

        self.assertEqual(buttons[0].get_attribute('href'), '{0}{1}'.format(self.live_server_url, export_url))

        # a button "Import"
        self.assertEqual(buttons[1].get_attribute('href'), self.live_server_url + self.url_import)

        # click on the button "Export"
        buttons[0].click()
        self.assertTrue(self.browser.current_url, self.live_server_url + export_url)

    def test_changelist_page_link_button_import_and_export_if_exist_objects(self):

        category1 = UtilityCategoryFactory(name='Category 1')
        category2 = UtilityCategoryFactory(name='Category 2')
        category3 = UtilityCategoryFactory(name='Category 3')

        # as well as, important sorting of queryset, make next tests
        list_pks = self.model.objects.values_list('pk', flat=True)
        self.assertEqual(len(list_pks), 3)
        self.assertIn(category1.pk, list_pks)
        self.assertIn(category2.pk, list_pks)
        self.assertIn(category3.pk, list_pks)

        self.open_page(self.url_changelist)

        buttons = self.browser.find_elements_by_xpath('//*[@id="changelist"]/div/div[1]/a')

        # a button "Export"
        export_url = self.reverse(
            'export_import_models:export',
            kwargs={
                'contenttype_model_pk': ContentType.objects.get_for_model(self.model).pk,
                'pks_separated_commas': ','.join(map(str, list_pks))
            }
        )

        self.assertEqual(buttons[0].get_attribute('href'), '{0}{1}'.format(self.live_server_url, export_url))

        # a button "Import"
        self.assertEqual(buttons[1].get_attribute('href'), self.live_server_url + self.url_import)

        # click on the button "Export"
        buttons[0].click()
        self.assertEqual(self.browser.current_url, self.live_server_url + export_url)


class UtilityAdminTest(StaticLiveAdminTest):

    @classmethod
    def setUpClass(cls):

        super().setUpClass()

        cls.url_changelist = cls.reverse('admin:utilities_utility_changelist')
        cls.url_import = cls.reverse('export_import_models:import')

        cls.categories = UtilityCategory.objects
        cls.model = UtilityFactory._meta.model

    def setUp(self):

        super().setUp()

        self.call_command('factory_test_users', '10')
        self.call_command('factory_test_categories_utilities', '2')

    def test_changelist_page_presents_three_buttons(self):

        self.open_page(self.url_changelist)

        buttons = self.browser.find_elements_by_xpath('//*[@id="changelist"]/div/div[1]/a')

        # 3 buttons: Export, Import, Add
        self.assertEqual(buttons[0].text, ' Export')
        self.assertEqual(buttons[1].text, ' Import')
        self.assertEqual(len(buttons), 3)

    def test_changelist_page_link_button_import_and_export_if_no_objects(self):

        self.open_page(self.url_changelist)

        buttons = self.browser.find_elements_by_xpath('//*[@id="changelist"]/div/div[1]/a')

        # link on this page, because not objects for export
        self.assertEqual(
            buttons[0].get_attribute('href'),
            self.live_server_url + self.url_changelist + '#'
        )

        # link for import objects
        self.assertEqual(
            buttons[1].get_attribute('href'),
            self.live_server_url + self.url_import
        )

        # click on button "Export" and page simple refresh
        buttons[0].click()
        self.assertTrue(self.browser.current_url.endswith('/#'.format(self.url_changelist)))

        # click on button "Import" and move to page for import
        buttons[1].click()
        self.assertEqual(self.browser.current_url, self.live_server_url + self.url_import)

    def test_changelist_page_link_button_import_and_export_if_exist_object(self):

        category = UtilityFactory()

        self.open_page(self.url_changelist)

        buttons = self.browser.find_elements_by_xpath('//*[@id="changelist"]/div/div[1]/a')

        # a button "Export"
        export_url = self.reverse(
            'export_import_models:export',
            kwargs={
                'contenttype_model_pk': ContentType.objects.get_for_model(self.model).pk,
                'pks_separated_commas': category.pk
            }
        )
        self.assertEqual(buttons[0].get_attribute('href'), '{0}{1}'.format(self.live_server_url, export_url))

        # a button "Import"
        self.assertEqual(buttons[1].get_attribute('href'), self.live_server_url + self.url_import)

        # click on the button "Export"
        buttons[0].click()
        self.assertTrue(self.browser.current_url, self.live_server_url + export_url)

    def test_changelist_page_link_button_import_and_export_if_exist_objects(self):

        utility1 = UtilityFactory()
        utility2 = UtilityFactory()
        utility3 = UtilityFactory()

        # as well as, important sorting of queryset, make next tests
        list_pks = self.model.objects.values_list('pk', flat=True)
        self.assertEqual(len(list_pks), 3)
        self.assertIn(utility1.pk, list_pks)
        self.assertIn(utility2.pk, list_pks)
        self.assertIn(utility3.pk, list_pks)

        self.open_page(self.url_changelist)

        buttons = self.browser.find_elements_by_xpath('//*[@id="changelist"]/div/div[1]/a')

        # a button "Export"
        export_url = self.reverse(
            'export_import_models:export',
            kwargs={
                'contenttype_model_pk': ContentType.objects.get_for_model(self.model).pk,
                'pks_separated_commas': ','.join(map(str, list_pks))
            }
        )
        self.assertEqual(buttons[0].get_attribute('href'), '{0}{1}'.format(self.live_server_url, export_url))

        # a button "Import"
        self.assertEqual(buttons[1].get_attribute('href'), self.live_server_url + self.url_import)

        # click on the button "Export"
        buttons[0].click()
        self.assertEqual(self.browser.current_url, self.live_server_url + export_url)
