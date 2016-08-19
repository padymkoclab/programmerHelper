
import io
from unittest import mock

from django.core.management import call_command

import pytest
from PyPDF2 import PdfFileReader

from mylabour.datetime_utils import (
    convert_date_to_django_date_format,
    get_current_timezone_offset,
    get_year_by_slavic_aryan_calendar
)
from mylabour.utils import get_location
from mylabour.test_utils import EnhancedTestCase

from config.admin import AdminSite
from apps.polls.models import Poll, Vote
from apps.polls.admin import PollAdmin
from apps.polls.factories import PollFactory, ChoiceFactory


class PollPDFReportWithoutObjectsTests(EnhancedTestCase):
    """
    Test for the PollPDFReport considering that polls, choices and votes
    does not exists yet.
    """

    @classmethod
    def setUpTestData(cls):

        # an active superuser for access to the admin
        call_command('factory_test_users', '1')
        cls.active_superuser = cls.django_user_model.objects.get()
        cls._make_user_as_active_superuser(cls.active_superuser)

        # full name of the user for check up in generated reports
        cls.superuser_full_name = cls.active_superuser.get_full_name()

        # django admin class
        cls.PollAdmin = PollAdmin(Poll, AdminSite)

        # url for make reports in PDF
        cls.url = cls.reverse('admin:polls_make_report')

    def setUp(self):

        # needed data of a POST request for generate PDF report
        self.data = {'output_report': 'report_pdf'}

        # in-memory file for PDF response
        self.buffer = io.BytesIO()

    def _get_text_for_empty_page_polls(self, number_page_in_doc):
        """Return text for page of polls considering number page if polls does not exists yet."""

        text = 'Report about polls\nPolls\nPage {0}\nSubject: Polls\nPolls are not exists yet\n'
        return text.format(number_page_in_doc)

    def _get_text_for_empty_page_choices(self, number_page_in_doc):
        """Return text for page of choices considering number page if choices does not exists yet."""

        text = 'Report about polls\nChoices\nPage {0}\nSubject: Choices\nChoices are not exists yet\n'
        return text.format(number_page_in_doc)

    def _get_text_for_empty_page_votes(self, number_page_in_doc):
        """Return text for page of votes considering number page if votes does not exists yet."""

        text = ''.join([
            'Report about polls\nVotes\nPage {0}\nSubject: Votes\nVotes are not exists yet\n'.format(
                number_page_in_doc
            ),
            '\n'.join([
                'Oct 2015',
                'Nov 2015',
                'Dec 2015',
                'Jan 2016',
                'Feb 2016',
                'Mar 2016',
                'Apr 2016',
                'May 2016',
                'Jun 2016',
                'Jul 2016',
                'Aug 2016',
                'Sep 2016',
            ]),
            '\n0 votes \n1 votes \n2 votes \n3 votes \n4 votes \n5 votes \n',
            '6 votes \n7 votes \n8 votes \n9 votes \n10 votes \n',
            '0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\nCount votes for the past year\n',
        ])
        return text.format(number_page_in_doc)

    def _get_text_for_empty_page_voters(self, number_page_in_doc):
        """Return text for page of voters considering number page if votes does not exists yet."""

        text = 'Report about polls\nVoters\nPage {0}\nSubject: Voters\nVotes are not exists yet\n'
        return text.format(number_page_in_doc)

    def _get_text_for_empty_page_results(self, number_page_in_doc):
        """Return text for page of results of polls considering number page if polls does not exists yet."""

        text = 'Report about polls\nResults of polls\nPage {0}\nSubject: Results of polls\nPolls are not exists yet\n'
        return text.format(number_page_in_doc)

    def _test_doc_info(self, doc, subject, count_pages):
        """Tests for an each generated report-document."""

        doc_info = doc.getDocumentInfo()
        self.assertEqual(doc.getNumPages(), count_pages)
        self.assertEqual(doc_info['/Creator'], self.settings.SITE_NAME)
        self.assertEqual(doc_info['/Keywords'], 'Polls, votes, voters')
        self.assertEqual(doc_info['/Subject'], subject)
        self.assertEqual(doc_info['/Title'], 'Report about polls')
        self.assertEqual(doc_info['/Author'], self.superuser_full_name)

    def _tests_title_page(self, doc, now, request):
        """Tests for a first (title) page of an each generated report."""

        page0Text = doc.getPage(0).extractText()

        self.assertIn(self.settings.SITE_NAME, page0Text)
        self.assertIn(
            '{0} A. D. ({1}'.format(
                now.year,
                get_year_by_slavic_aryan_calendar(now)
            ),
            page0Text
        )
        self.assertIn('Report', page0Text)
        self.assertIn('"Report about polls"', page0Text)

        location = get_location(request)
        if location is None:
            location = '(Not possible determinate location)'
        self.assertIn('Location: (Not possible determinate location)'.format(location), page0Text)
        self.assertIn('Author: {0}'.format(self.superuser_full_name), page0Text)
        self.assertIn(
            'Generated: {0}'.format(convert_date_to_django_date_format(now)),
            page0Text
        )
        self.assertIn(
            'Timezone: Europe/Kiev ({1})'.format(
                self.settings.TIME_ZONE,
                get_current_timezone_offset()
            ),
            page0Text
        )

    def _tests_content_page(self, doc, themes):
        """Tests for a second page in an each generated report."""

        page1Text = doc.getPage(1).extractText()
        listing_themes = '\n'.join(themes)
        self.assertEqual(
            ''.join([
                'Report about polls\nContent\nPage 2\nContent of report\n',
                'This report contains a next subject:\n{0}\n'.format(listing_themes),
            ]),
            page1Text
        )

    def _test_statistics_page(self, doc):
        """Tests for a third page - statistics of an each generated report."""

        page2Text = doc.getPage(2).extractText()
        self.assertEqual(
            ''.join([
                'Report about polls\nStatistics\nPage 3\nStatictics\nCount polls\n0\nCount opened polls\n0\n',
                'Count closed polls\n0\nCount draft polls\n0\nCount choices\n0\nCount votes\n0\nCount voters\n0\n',
                'Average a count votes in the polls\n0.0\nAverage a count choices in the polls\n0.0\n',
                'Date a latest vote\n\nA latest voter\n\nA poll with the latest vote\n\nA latest selected choice\n\n'
            ]),
            page2Text
        )

    @mock.patch('django.utils.timezone.now')
    def _get_doc_from_request_and_now_and_request(self, mock_now):
        """Return a generated PDF in in-memory file, now datetime and request."""

        # mock current datetime
        mock_now.return_value = self.timezone.datetime(2016, 9, 22, tzinfo=self.timezone.utc)

        request = self.factory.post(self.url, self.data)
        request.user = self.active_superuser

        now = self.timezone.now()

        response = self.PollAdmin.view_make_report(request)

        self.buffer.write(response.getvalue())

        doc = PdfFileReader(self.buffer)

        return doc, now, request

    def test_without_objects_on_theme_polls(self):

        self.data['polls'] = 'polls'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls', 4)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

    def test_without_objects_on_theme_choices(self):

        self.data['choices'] = 'choices'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Choices', 4)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Choices'])
        self._test_statistics_page(doc)

        # page of choices
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

    def test_without_objects_on_theme_votes(self):

        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Votes', 4)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Votes'])
        self._test_statistics_page(doc)

        # page of votes
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

    def test_without_objects_on_theme_voters(self):

        self.data['voters'] = 'voters'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Voters', 4)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Voters'])
        self._test_statistics_page(doc)

        # page of voters
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

    def test_without_objects_on_theme_results(self):

        self.data['results'] = 'results'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Results of polls', 4)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Results of polls'])
        self._test_statistics_page(doc)

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

    def test_without_objects_on_theme_polls_and_choices(self):

        self.data['polls'] = 'polls'
        self.data['choices'] = 'choices'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, choices', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Choices'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of choices
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    def test_without_objects_on_theme_polls_and_votes(self):

        self.data['polls'] = 'polls'
        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, votes', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Votes'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of votes
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    def test_without_objects_on_theme_polls_and_voters(self):

        self.data['polls'] = 'polls'
        self.data['voters'] = 'voters'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, voters', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Voters'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of voters
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    def test_without_objects_on_theme_polls_and_results(self):

        self.data['polls'] = 'polls'
        self.data['results'] = 'results'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, results of polls', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    def test_without_objects_on_theme_choices_and_votes(self):

        self.data['choices'] = 'choices'
        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Choices, votes', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Choices', 'Votes'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    def test_without_objects_on_theme_choices_and_voters(self):

        self.data['choices'] = 'choices'
        self.data['voters'] = 'voters'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Choices, voters', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Choices', 'Voters'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    def test_without_objects_on_theme_choices_and_results(self):

        self.data['choices'] = 'choices'
        self.data['results'] = 'results'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Choices, results of polls', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Choices', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    def test_without_objects_on_theme_votes_and_voters(self):

        self.data['votes'] = 'votes'
        self.data['voters'] = 'voters'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Votes, voters', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Votes', 'Voters'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    def test_without_objects_on_theme_votes_and_results(self):

        self.data['votes'] = 'votes'
        self.data['results'] = 'results'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Votes, results of polls', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Votes', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    def test_without_objects_on_theme_voters_and_results(self):

        self.data['voters'] = 'voters'
        self.data['results'] = 'results'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Voters, results of polls', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Voters', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    def test_without_objects_on_theme_polls_and_choices_and_results(self):

        self.data['polls'] = 'polls'
        self.data['results'] = 'results'
        self.data['choices'] = 'choices'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, choices, results of polls', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Choices', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    def test_without_objects_on_theme_polls_and_choices_and_votes(self):

        self.data['polls'] = 'polls'
        self.data['votes'] = 'votes'
        self.data['choices'] = 'choices'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, choices, votes', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Choices', 'Votes'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    def test_without_objects_on_theme_polls_and_choices_and_voters(self):

        self.data['polls'] = 'polls'
        self.data['voters'] = 'voters'
        self.data['choices'] = 'choices'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, choices, voters', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Choices', 'Voters'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    def test_without_objects_on_theme_polls_and_votes_and_voters(self):

        self.data['polls'] = 'polls'
        self.data['voters'] = 'voters'
        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, votes, voters', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Votes', 'Voters'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    def test_without_objects_on_theme_polls_and_votes_results(self):

        self.data['polls'] = 'polls'
        self.data['votes'] = 'votes'
        self.data['results'] = 'results'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, votes, results of polls', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Votes', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    def test_without_objects_on_theme_polls_and_voters_results(self):

        self.data['polls'] = 'polls'
        self.data['voters'] = 'voters'
        self.data['results'] = 'results'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, voters, results of polls', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Voters', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    def test_without_objects_on_theme_choices_and_votes_and_voters(self):

        self.data['choices'] = 'choices'
        self.data['voters'] = 'voters'
        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Choices, votes, voters', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Choices', 'Votes', 'Voters'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    def test_without_objects_on_theme_choices_and_votes_and_results(self):

        self.data['choices'] = 'choices'
        self.data['results'] = 'results'
        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Choices, votes, results of polls', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Choices', 'Votes', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    def test_without_objects_on_theme_choices_and_voters_and_results(self):

        self.data['choices'] = 'choices'
        self.data['voters'] = 'voters'
        self.data['results'] = 'results'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Choices, voters, results of polls', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Choices', 'Voters', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    def test_without_objects_on_theme_votes_and_voters_and_results(self):

        self.data['results'] = 'results'
        self.data['voters'] = 'voters'
        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Votes, voters, results of polls', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Votes', 'Voters', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    def test_without_objects_on_theme_polls_and_choices_and_votes_and_voters(self):

        self.data['polls'] = 'polls'
        self.data['choices'] = 'choices'
        self.data['voters'] = 'voters'
        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, choices, votes, voters', 7)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Choices', 'Votes', 'Voters'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=7),
            doc.getPage(6).extractText()
        )

    def test_without_objects_on_theme_polls_and_choices_and_votes_and_results(self):

        self.data['polls'] = 'polls'
        self.data['choices'] = 'choices'
        self.data['results'] = 'results'
        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, choices, votes, results of polls', 7)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Choices', 'Votes', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=7),
            doc.getPage(6).extractText()
        )

    def test_without_objects_on_theme_polls_and_choices_votes_and_voters(self):

        self.data['polls'] = 'polls'
        self.data['choices'] = 'choices'
        self.data['voters'] = 'voters'
        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, choices, votes, voters', 7)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Choices', 'Votes', 'Voters'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=7),
            doc.getPage(6).extractText()
        )

    def test_without_objects_on_theme_polls_and_choices_and_voters_and_results(self):

        self.data['polls'] = 'polls'
        self.data['choices'] = 'choices'
        self.data['results'] = 'results'
        self.data['voters'] = 'voters'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, choices, voters, results of polls', 7)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Choices', 'Voters', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=7),
            doc.getPage(6).extractText()
        )

    def test_without_objects_on_theme_choices_and_votes_voters_and_results(self):

        self.data['votes'] = 'votes'
        self.data['choices'] = 'choices'
        self.data['results'] = 'results'
        self.data['voters'] = 'voters'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Choices, votes, voters, results of polls', 7)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Choices', 'Votes', 'Voters', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=7),
            doc.getPage(6).extractText()
        )

    def test_without_objects_on_theme_polls_and_choices_and_votes_and_voters_and_results(self):

        self.data['polls'] = 'polls'
        self.data['votes'] = 'votes'
        self.data['choices'] = 'choices'
        self.data['results'] = 'results'
        self.data['voters'] = 'voters'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, choices, votes, voters, results of polls', 8)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Choices', 'Votes', 'Voters', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=7),
            doc.getPage(6).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=8),
            doc.getPage(7).extractText()
        )


class PollPDFReportWithObjectsTests(EnhancedTestCase):
    """
    Test for the PollPDFReport considering that polls, choices and votes
    does not exists yet.
    """

    @classmethod
    def setUpTestData(cls):

        # an active superuser for access to the admin
        call_command('factory_test_users', '4')
        cls.active_superuser, cls.user1, cls.user2, cls.user3 = cls.django_user_model.objects.all()
        cls._make_user_as_active_superuser(cls.active_superuser)

        # full name of the user for check up in generated reports
        cls.superuser_full_name = cls.active_superuser.get_full_name()

        # generate polls, choices and votes
        cls.poll1 = PollFactory(status='opened')
        cls.choice11 = ChoiceFactory(poll=cls.poll1)
        cls.choice12 = ChoiceFactory(poll=cls.poll1)
        cls.choice13 = ChoiceFactory(poll=cls.poll1)

        cls.poll2 = PollFactory(status='draft')
        cls.choice21 = ChoiceFactory(poll=cls.poll2)
        cls.choice22 = ChoiceFactory(poll=cls.poll2)

        cls.poll3 = PollFactory(status='draft')
        cls.choice31 = ChoiceFactory(poll=cls.poll3)

        cls.poll4 = PollFactory(status='opened')
        cls.poll5 = PollFactory(status='opened')

        Vote.objects.create(user=cls.active_superuser, poll=cls.poll1, choice=cls.choice11)
        Vote.objects.create(user=cls.user1, poll=cls.poll1, choice=cls.choice11)
        Vote.objects.create(user=cls.user1, poll=cls.poll2, choice=cls.choice21)
        Vote.objects.create(user=cls.user2, poll=cls.poll1, choice=cls.choice21)
        Vote.objects.create(user=cls.user2, poll=cls.poll2, choice=cls.choice22)
        Vote.objects.create(user=cls.active_superuser, poll=cls.poll2, choice=cls.choice21)
        cls.vote = Vote.objects.create(user=cls.user2, poll=cls.poll3, choice=cls.choice31)

        # django admin class
        cls.PollAdmin = PollAdmin(Poll, AdminSite)

        # url for make reports in PDF
        cls.url = cls.reverse('admin:polls_make_report')

    def setUp(self):

        # needed data of a POST request for generate PDF report
        self.data = {'output_report': 'report_pdf'}

        # in-memory file for PDF response
        self.buffer = io.BytesIO()

    def _get_text_for_empty_page_polls(self, number_page_in_doc):
        """Return text for page of polls considering number page if polls does not exists yet."""

        text = 'Report about polls\nPolls\nPage {0}\nSubject: Polls\nPolls are not exists yet\n'
        return text.format(number_page_in_doc)

    def _get_text_for_empty_page_choices(self, number_page_in_doc):
        """Return text for page of choices considering number page if choices does not exists yet."""

        text = 'Report about polls\nChoices\nPage {0}\nSubject: Choices\nChoices are not exists yet\n'
        return text.format(number_page_in_doc)

    def _get_text_for_empty_page_votes(self, number_page_in_doc):
        """Return text for page of votes considering number page if votes does not exists yet."""

        text = ''.join([
            'Report about polls\nVotes\nPage {0}\nSubject: Votes\nVotes are not exists yet\n'.format(
                number_page_in_doc
            ),
            '\n'.join([
                'Oct 2015',
                'Nov 2015',
                'Dec 2015',
                'Jan 2016',
                'Feb 2016',
                'Mar 2016',
                'Apr 2016',
                'May 2016',
                'Jun 2016',
                'Jul 2016',
                'Aug 2016',
                'Sep 2016',
            ]),
            '\n0 votes \n1 votes \n2 votes \n3 votes \n4 votes \n5 votes \n',
            '6 votes \n7 votes \n8 votes \n9 votes \n10 votes \n',
            '0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\nCount votes for the past year\n',
        ])
        return text.format(number_page_in_doc)

    def _get_text_for_empty_page_voters(self, number_page_in_doc):
        """Return text for page of voters considering number page if votes does not exists yet."""

        text = 'Report about polls\nVoters\nPage {0}\nSubject: Voters\nVotes are not exists yet\n'
        return text.format(number_page_in_doc)

    def _get_text_for_empty_page_results(self, number_page_in_doc):
        """Return text for page of results of polls considering number page if polls does not exists yet."""

        text = 'Report about polls\nResults of polls\nPage {0}\nSubject: Results of polls\nPolls are not exists yet\n'
        return text.format(number_page_in_doc)

    def _test_doc_info(self, doc, subject, count_pages):
        """Tests for an each generated report-document."""

        doc_info = doc.getDocumentInfo()
        self.assertEqual(doc.getNumPages(), count_pages)
        self.assertEqual(doc_info['/Creator'], self.settings.SITE_NAME)
        self.assertEqual(doc_info['/Keywords'], 'Polls, votes, voters')
        self.assertEqual(doc_info['/Subject'], subject)
        self.assertEqual(doc_info['/Title'], 'Report about polls')
        self.assertEqual(doc_info['/Author'], self.superuser_full_name)

    def _tests_title_page(self, doc, now, request):
        """Tests for a first (title) page of an each generated report."""

        page0Text = doc.getPage(0).extractText()

        self.assertIn(self.settings.SITE_NAME, page0Text)
        self.assertIn(
            '{0} A. D. ({1}'.format(
                now.year,
                get_year_by_slavic_aryan_calendar(now)
            ),
            page0Text
        )
        self.assertIn('Report', page0Text)
        self.assertIn('"Report about polls"', page0Text)

        location = get_location(request)
        if location is None:
            location = '(Not possible determinate location)'
        self.assertIn('Location: (Not possible determinate location)'.format(location), page0Text)
        self.assertIn('Author: {0}'.format(self.superuser_full_name), page0Text)
        self.assertIn('Generated: {0}'.format(convert_date_to_django_date_format(now)), page0Text)
        self.assertIn(
            'Timezone: Europe/Kiev ({1})'.format(
                self.settings.TIME_ZONE,
                get_current_timezone_offset()
            ),
            page0Text
        )

    def _tests_content_page(self, doc, themes):
        """Tests for a second page in an each generated report."""

        page1Text = doc.getPage(1).extractText()
        listing_themes = '\n'.join(themes)
        self.assertEqual(
            ''.join([
                'Report about polls\nContent\nPage 2\nContent of report\n',
                'This report contains a next subject:\n{0}\n'.format(listing_themes),
            ]),
            page1Text
        )

    def _test_statistics_page(self, doc):

        page2Text = doc.getPage(2).extractText()
        self.assertEqual(
            ''.join([
                'Report about polls\nStatistics\nPage 3\nStatictics\nCount polls\n5\nCount opened polls\n3\n',
                'Count closed polls\n0\nCount draft polls\n2\nCount choices\n6\nCount votes\n7\nCount voters\n3\n',
                'Average a count votes in the polls\n1.4\nAverage a count choices in the polls\n1.2\n',
                'Date a latest vote\n{0}\nA latest voter\n{1}\n'.format(
                    convert_date_to_django_date_format(self.vote.date_voting),
                    self.user2.get_full_name(),
                ),
                'A poll with the latest vote\n{0}\nA latest selected choice\n{0}\n'.format(
                    self.vote.poll,
                    self.vote.choice,
                )
            ]),
            page2Text
        )

    @mock.patch('django.utils.timezone.now')
    def _get_doc_from_request_and_now_and_request(self, mock_now):
        """Return a generated PDF in in-memory file, now datetime and request."""

        # mock current datetime
        mock_now.return_value = self.timezone.datetime(2016, 9, 22, tzinfo=self.timezone.utc)

        request = self.factory.post(self.url, self.data)
        request.user = self.active_superuser

        now = self.timezone.now()

        response = self.PollAdmin.view_make_report(request)

        self.buffer.write(response.getvalue())

        doc = PdfFileReader(self.buffer)

        return doc, now, request

    @pytest.mark.skip('Does not working with unicode')
    def test_without_objects_on_theme_polls(self):

        self.data['polls'] = 'polls'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_choices(self):

        self.data['choices'] = 'choices'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Choices', 4)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Choices'])
        self._test_statistics_page(doc)

        # page of choices
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_votes(self):

        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Votes', 4)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Votes'])
        self._test_statistics_page(doc)

        # page of votes
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_voters(self):

        self.data['voters'] = 'voters'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Voters', 4)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Voters'])
        self._test_statistics_page(doc)

        # page of voters
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_results(self):

        self.data['results'] = 'results'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Results of polls', 4)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Results of polls'])
        self._test_statistics_page(doc)

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_polls_and_choices(self):

        self.data['polls'] = 'polls'
        self.data['choices'] = 'choices'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, choices', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Choices'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of choices
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_polls_and_votes(self):

        self.data['polls'] = 'polls'
        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, votes', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Votes'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of votes
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_polls_and_voters(self):

        self.data['polls'] = 'polls'
        self.data['voters'] = 'voters'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, voters', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Voters'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of voters
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_polls_and_results(self):

        self.data['polls'] = 'polls'
        self.data['results'] = 'results'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, results of polls', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_choices_and_votes(self):

        self.data['choices'] = 'choices'
        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Choices, votes', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Choices', 'Votes'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_choices_and_voters(self):

        self.data['choices'] = 'choices'
        self.data['voters'] = 'voters'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Choices, voters', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Choices', 'Voters'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_choices_and_results(self):

        self.data['choices'] = 'choices'
        self.data['results'] = 'results'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Choices, results of polls', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Choices', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_votes_and_voters(self):

        self.data['votes'] = 'votes'
        self.data['voters'] = 'voters'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Votes, voters', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Votes', 'Voters'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_votes_and_results(self):

        self.data['votes'] = 'votes'
        self.data['results'] = 'results'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Votes, results of polls', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Votes', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_voters_and_results(self):

        self.data['voters'] = 'voters'
        self.data['results'] = 'results'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Voters, results of polls', 5)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Voters', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_polls_and_choices_and_results(self):

        self.data['polls'] = 'polls'
        self.data['results'] = 'results'
        self.data['choices'] = 'choices'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, choices, results of polls', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Choices', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_polls_and_choices_and_votes(self):

        self.data['polls'] = 'polls'
        self.data['votes'] = 'votes'
        self.data['choices'] = 'choices'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, choices, votes', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Choices', 'Votes'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_polls_and_choices_and_voters(self):

        self.data['polls'] = 'polls'
        self.data['voters'] = 'voters'
        self.data['choices'] = 'choices'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, choices, voters', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Choices', 'Voters'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_polls_and_votes_and_voters(self):

        self.data['polls'] = 'polls'
        self.data['voters'] = 'voters'
        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, votes, voters', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Votes', 'Voters'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_polls_and_votes_results(self):

        self.data['polls'] = 'polls'
        self.data['votes'] = 'votes'
        self.data['results'] = 'results'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, votes, results of polls', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Votes', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_polls_and_voters_results(self):

        self.data['polls'] = 'polls'
        self.data['voters'] = 'voters'
        self.data['results'] = 'results'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, voters, results of polls', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Voters', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_choices_and_votes_and_voters(self):

        self.data['choices'] = 'choices'
        self.data['voters'] = 'voters'
        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Choices, votes, voters', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Choices', 'Votes', 'Voters'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_choices_and_votes_and_results(self):

        self.data['choices'] = 'choices'
        self.data['results'] = 'results'
        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Choices, votes, results of polls', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Choices', 'Votes', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_choices_and_voters_and_results(self):

        self.data['choices'] = 'choices'
        self.data['voters'] = 'voters'
        self.data['results'] = 'results'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Choices, voters, results of polls', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Choices', 'Voters', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_votes_and_voters_and_results(self):

        self.data['results'] = 'results'
        self.data['voters'] = 'voters'
        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Votes, voters, results of polls', 6)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Votes', 'Voters', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )

        # page of results
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_polls_and_choices_and_votes_and_voters(self):

        self.data['polls'] = 'polls'
        self.data['choices'] = 'choices'
        self.data['voters'] = 'voters'
        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, choices, votes, voters', 7)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Choices', 'Votes', 'Voters'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=7),
            doc.getPage(6).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_polls_and_choices_and_votes_and_results(self):

        self.data['polls'] = 'polls'
        self.data['choices'] = 'choices'
        self.data['results'] = 'results'
        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, choices, votes, results of polls', 7)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Choices', 'Votes', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=7),
            doc.getPage(6).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_polls_and_choices_votes_and_voters(self):

        self.data['polls'] = 'polls'
        self.data['choices'] = 'choices'
        self.data['voters'] = 'voters'
        self.data['votes'] = 'votes'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, choices, votes, voters', 7)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Choices', 'Votes', 'Voters'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=7),
            doc.getPage(6).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_polls_and_choices_and_voters_and_results(self):

        self.data['polls'] = 'polls'
        self.data['choices'] = 'choices'
        self.data['results'] = 'results'
        self.data['voters'] = 'voters'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, choices, voters, results of polls', 7)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Choices', 'Voters', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=7),
            doc.getPage(6).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_choices_and_votes_voters_and_results(self):

        self.data['votes'] = 'votes'
        self.data['choices'] = 'choices'
        self.data['results'] = 'results'
        self.data['voters'] = 'voters'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Choices, votes, voters, results of polls', 7)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Choices', 'Votes', 'Voters', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=7),
            doc.getPage(6).extractText()
        )

    @pytest.mark.xfail(run=False)
    def test_without_objects_on_theme_polls_and_choices_and_votes_and_voters_and_results(self):

        self.data['polls'] = 'polls'
        self.data['votes'] = 'votes'
        self.data['choices'] = 'choices'
        self.data['results'] = 'results'
        self.data['voters'] = 'voters'

        doc, now, request = self._get_doc_from_request_and_now_and_request()

        self._test_doc_info(doc, 'Polls, choices, votes, voters, results of polls', 8)
        self._tests_title_page(doc, now, request)
        self._tests_content_page(doc, ['Polls', 'Choices', 'Votes', 'Voters', 'Results of polls'])
        self._test_statistics_page(doc)

        self.assertEqual(
            self._get_text_for_empty_page_polls(number_page_in_doc=4),
            doc.getPage(3).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_choices(number_page_in_doc=5),
            doc.getPage(4).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_votes(number_page_in_doc=6),
            doc.getPage(5).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_voters(number_page_in_doc=7),
            doc.getPage(6).extractText()
        )
        self.assertEqual(
            self._get_text_for_empty_page_results(number_page_in_doc=8),
            doc.getPage(7).extractText()
        )
