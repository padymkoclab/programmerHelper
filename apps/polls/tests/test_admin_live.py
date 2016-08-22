
from mylabour.test_utils import StaticLiveAdminTest

from config.admin import AdminSite

from apps.polls.models import Poll
from apps.polls.admin import PollAdmin

# invoke git_push "Started writing live tests for the app 'polls'."


class PollAdminLiveTests(StaticLiveAdminTest):

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

        self.assertFalse(self.browser.find_element_by_name('polls').is_selected())
        self.assertFalse(self.browser.find_element_by_name('choices').is_selected())
        self.assertFalse(self.browser.find_element_by_name('votes').is_selected())
        self.assertTrue(self.browser.find_element_by_name('results').is_selected())
        self.assertFalse(self.browser.find_element_by_name('voters').is_selected())

    def test_page_polls_statistics(self):

        url = self.reverse('admin:polls_statistics')
        self.open_page(url)

        admin_breadcrumb_ul = self.browser.find_element_by_xpath('//*[@id="suit-center"]/ul')
        lis = admin_breadcrumb_ul.find_elements_by_tag_name('li')

        self.assertEqual(lis[0].find_element_by_tag_name('a').text, 'Home')
        self.assertEqual(lis[1].find_element_by_tag_name('a').text, 'Polls')
        self.assertEqual(lis[2].find_element_by_tag_name('a').text, 'Make a report about polls')
        self.assertEqual(lis[2].find_element_by_tag_name('a').get_attribute('class'), 'activate')
