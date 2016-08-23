
from mylabour.test_utils import StaticLiveAdminTest

from apps.polls.factories import PollFactory, ChoiceFactory
from apps.polls.models import Poll


class PollAdminLiveTests(StaticLiveAdminTest):

    def tearDown(self):
        super(PollAdminLiveTests, self).tearDown()
        Poll.objects.filter().delete()

    def test_page_app_index_polls(self):

        url = self.reverse('admin:app_list', kwargs={'app_label': 'polls'})
        self.open_page(url)

        self.browser.find_element_by_xpath('//*[@id="content-main"]/div/table/tbody/tr[1]/td[1]/a').click()
        self.assertIn(self.reverse('admin:polls_choice_changelist'), self.browser.current_url)

        self.open_page(url)
        self.browser.find_element_by_xpath('//*[@id="content-main"]/div/table/tbody/tr[2]/td[1]/a').click()
        self.assertIn(self.reverse('admin:polls_poll_changelist'), self.browser.current_url)

        self.open_page(url)
        self.browser.find_element_by_xpath('//*[@id="content-main"]/div/table/tbody/tr[2]/td[2]/a').click()
        self.assertIn(self.reverse('admin:polls_poll_add'), self.browser.current_url)

        self.open_page(url)
        self.browser.find_element_by_xpath('//*[@id="content-main"]/div/table/tbody/tr[3]/td[1]/a').click()
        self.assertIn(self.reverse('admin:polls_vote_changelist'), self.browser.current_url)

        self.open_page(url)
        self.browser.find_element_by_xpath('//*[@id="content-main"]/div/table/tbody/tr[4]/td[1]/a').click()
        self.assertIn(self.reverse('admin:users_user_changelist'), self.browser.current_url)

        self.open_page(url)
        self.browser.find_element_by_xpath('//*[@id="content-summary"]/table/tbody/tr[1]/td[1]/a').click()
        self.assertIn(self.reverse('admin:polls_make_report'), self.browser.current_url)

        self.open_page(url)
        self.browser.find_element_by_xpath('//*[@id="content-summary"]/table/tbody/tr[2]/td[1]/a').click()
        self.assertIn(self.reverse('admin:polls_statistics'), self.browser.current_url)

    def test_page_polls_make_report(self):

        url = self.reverse('admin:polls_make_report')
        self.open_page(url)

        # test breadcrum menu
        ul_breadcrumb = self.browser.find_element_by_xpath('//*[@id="suit-center"]/ul')

        self.assertEqual(ul_breadcrumb.find_elements_by_css_selector('li a')[0].text, 'Home')
        self.assertEqual(ul_breadcrumb.find_elements_by_css_selector('li a')[1].text, 'Polls')
        self.assertEqual(ul_breadcrumb.find_elements_by_css_selector('li')[2].text, 'Make a report about polls')
        self.assertEqual(ul_breadcrumb.find_elements_by_css_selector('li')[2].get_attribute('class'), 'active')

        # test disalabling btn if not activate no-one checkbox
        checkbox_results = self.browser.find_element_by_name('results')
        btn_submit_create_report = self.browser.find_element_by_xpath('//*[@id="btn_submit_make_report_polls"]')

        # single checkbox is activated
        self.assertFalse(self.browser.find_element_by_name('polls').is_selected())
        self.assertFalse(self.browser.find_element_by_name('choices').is_selected())
        self.assertFalse(self.browser.find_element_by_name('votes').is_selected())
        self.assertTrue(checkbox_results.is_selected())
        self.assertFalse(self.browser.find_element_by_name('voters').is_selected())

        # btn must be activated
        self.assertIsNone(btn_submit_create_report.get_attribute('disabled'))

        # disable latest activated chackbox
        checkbox_results.click()

        # all checkboxes is disabled
        self.assertFalse(self.browser.find_element_by_name('polls').is_selected())
        self.assertFalse(self.browser.find_element_by_name('choices').is_selected())
        self.assertFalse(self.browser.find_element_by_name('votes').is_selected())
        self.assertFalse(checkbox_results.is_selected())
        self.assertFalse(self.browser.find_element_by_name('voters').is_selected())

        # btn must be disabled
        self.assertEqual(btn_submit_create_report.get_attribute('disabled'), 'true')

    def test_page_polls_statistics(self):

        url = self.reverse('admin:polls_statistics')
        self.open_page(url)

        admin_breadcrumb_ul = self.browser.find_element_by_xpath('//*[@id="suit-center"]/ul')
        lis = admin_breadcrumb_ul.find_elements_by_tag_name('li')

        self.assertEqual(lis[0].find_element_by_tag_name('a').text, 'Home')
        self.assertEqual(lis[1].find_element_by_tag_name('a').text, 'Polls')
        self.assertEqual(lis[2].text, 'Statistics about polls')
        self.assertEqual(lis[2].get_attribute('class'), 'active')

    def test_page_change_exists_poll_with_stacked_choices(self):

        poll = PollFactory(title='name' * 21)
        ChoiceFactory(poll=poll, text_choice='text' * 20)
        ChoiceFactory(poll=poll, text_choice='text' * 21)

        url = self.reverse('admin:polls_poll_change', args=(poll.pk, ))
        self.open_page(url)

        # length a poll`s title
        self.assertEqual(len(self.browser.find_element_by_xpath('//*[@id="suit-center"]/ul/li[4]').text), 80)

        # lengths a texts of choices of the poll
        self.assertEqual(len(self.browser.find_element_by_xpath('//*[@id="choices-0"]/h3/span[1]').text), 80)
        self.assertEqual(len(self.browser.find_element_by_xpath('//*[@id="choices-1"]/h3/span[1]').text), 80)

    def test_page_polls_changelist(self):

        url = self.reverse('admin:polls_poll_changelist')
        self.open_page(url)

        btn_links = self.browser.find_element_by_xpath('//*[@id="changelist"]/div/div[1]').\
            find_elements_by_tag_name('a')

        # btn export polls
        self.assertEqual(btn_links[0].text, ' Export')
        self.assertEqual(btn_links[0].get_attribute('href'), '{0}#'.format(self.browser.current_url))

        # btn import polls
        self.assertEqual(btn_links[1].text, ' Import')
        self.assertEqual(
            btn_links[1].get_attribute('href'),
            '{0}{1}'.format(self.live_server_url, self.reverse('export_import_models:import'))
        )

        # btn add a poll
        url_add_poll = '{0}{1}'.format(self.live_server_url, self.reverse('admin:polls_poll_add'))
        self.assertEqual(btn_links[2].get_attribute('href'), url_add_poll)

        # if polls are not exists
        self.assertEqual(
            self.browser.find_element_by_xpath('//*[@id="changelist-form"]/div/a').get_attribute('href'),
            url_add_poll,
        )

    def test_page_choices_changelist(self):

        url = self.reverse('admin:polls_choice_changelist')
        self.open_page(url)

        btn_links = self.browser.find_element_by_xpath('//*[@id="changelist"]/div/div[1]').\
            find_elements_by_tag_name('a')

        # btn export choices
        self.assertEqual(btn_links[0].text, ' Export')
        self.assertEqual(btn_links[0].get_attribute('href'), '{0}#'.format(self.browser.current_url))

        # btn import choices
        self.assertEqual(btn_links[1].text, ' Import')
        self.assertEqual(
            btn_links[1].get_attribute('href'),
            '{0}{1}'.format(self.live_server_url, self.reverse('export_import_models:import'))
        )

        # btn add a choice does not exists
        self.assertRaises(IndexError, btn_links.__getitem__, 2)

        # if choices are not exists
        self.assertEqual(len(self.browser.find_elements_by_xpath('//*[@id="changelist-form"]/div/a')), 0)

    def test_page_choices_change(self):

        poll = PollFactory()
        choice = ChoiceFactory(poll=poll, text_choice='text' * 25)

        url = self.reverse('admin:polls_choice_change', args=(choice.pk, ))
        self.open_page(url)

        self.assertEqual(len(self.browser.find_element_by_xpath('//*[@id="suit-center"]/ul/li[4]').text), 80)

        self.assertEqual(
            self.browser.find_element_by_xpath('//*[@id="content-main"]/form/div[1]').get_attribute('innerHTML'),
            ''
        )

    def test_page_votes_changelist(self):

        url = self.reverse('admin:polls_vote_changelist')
        self.open_page(url)

        btn_links = self.browser.find_element_by_xpath('//*[@id="changelist"]/div/div[1]').\
            find_elements_by_tag_name('a')

        # btn export polls
        self.assertEqual(btn_links[0].text, ' Export')
        self.assertEqual(btn_links[0].get_attribute('href'), '{0}#'.format(self.browser.current_url))

        # btn import polls
        self.assertEqual(btn_links[1].text, ' Import')
        self.assertEqual(
            btn_links[1].get_attribute('href'),
            '{0}{1}'.format(self.live_server_url, self.reverse('export_import_models:import'))
        )

        # btn add a votes does not exists
        self.assertRaises(IndexError, btn_links.__getitem__, 2)

        # if votes are not exists
        self.assertEqual(len(self.browser.find_elements_by_xpath('//*[@id="changelist-form"]/div/a')), 0)


class ChoiceAdminLiveTests(StaticLiveAdminTest):

    def tearDown(self):
        super(ChoiceAdminLiveTests, self).tearDown()
        Poll.objects.filter().delete()

    def test_page_choices_changelist(self):

        url = self.reverse('admin:polls_choice_changelist')
        self.open_page(url)

        btn_links = self.browser.find_element_by_xpath('//*[@id="changelist"]/div/div[1]').\
            find_elements_by_tag_name('a')

        # btn export choices
        self.assertEqual(btn_links[0].text, ' Export')
        self.assertEqual(btn_links[0].get_attribute('href'), '{0}#'.format(self.browser.current_url))

        # btn import choices
        self.assertEqual(btn_links[1].text, ' Import')
        self.assertEqual(
            btn_links[1].get_attribute('href'),
            '{0}{1}'.format(self.live_server_url, self.reverse('export_import_models:import'))
        )

        # btn add a choice does not exists
        self.assertRaises(IndexError, btn_links.__getitem__, 2)

        # if choices are not exists
        self.assertEqual(len(self.browser.find_elements_by_xpath('//*[@id="changelist-form"]/div/a')), 0)

    def test_page_choices_change(self):

        poll = PollFactory()
        choice = ChoiceFactory(poll=poll, text_choice='text' * 25)

        url = self.reverse('admin:polls_choice_change', args=(choice.pk, ))
        self.open_page(url)

        self.assertEqual(len(self.browser.find_element_by_xpath('//*[@id="suit-center"]/ul/li[4]').text), 80)

        self.assertEqual(
            self.browser.find_element_by_xpath('//*[@id="content-main"]/form/div[1]').get_attribute('innerHTML'),
            ''
        )


class VoteAdminLiveTests(StaticLiveAdminTest):

    def test_page_votes_changelist(self):

        url = self.reverse('admin:polls_vote_changelist')
        self.open_page(url)

        btn_links = self.browser.find_element_by_xpath('//*[@id="changelist"]/div/div[1]').\
            find_elements_by_tag_name('a')

        # btn export polls
        self.assertEqual(btn_links[0].text, ' Export')
        self.assertEqual(btn_links[0].get_attribute('href'), '{0}#'.format(self.browser.current_url))

        # btn import polls
        self.assertEqual(btn_links[1].text, ' Import')
        self.assertEqual(
            btn_links[1].get_attribute('href'),
            '{0}{1}'.format(self.live_server_url, self.reverse('export_import_models:import'))
        )

        # btn add a votes does not exists
        self.assertRaises(IndexError, btn_links.__getitem__, 2)

        # if votes are not exists
        self.assertEqual(len(self.browser.find_elements_by_xpath('//*[@id="changelist-form"]/div/a')), 0)
