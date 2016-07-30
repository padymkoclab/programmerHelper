from io import BytesIO
import logging
import random
import textwrap

from django.utils.translation import ugettext as _
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.conf import settings

from reportlab.lib import colors
from reportlab.platypus import (
    Paragraph,
    PageBreak,
    NextPageTemplate,
    Table,
    TableStyle,
)
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.widgets.markers import makeMarker

import xlsxwriter

from apps.core.reports import SitePDFReportTemplate
from mylabour.utils import (
    get_filename_with_datetime,
    convert_date_to_django_date_format,
    get_latest_or_none,
    create_logger_by_filename
)

from apps.polls.models import Poll, Choice, VoteInPoll


User = get_user_model()
logger = create_logger_by_filename(__name__)


class ExcelReport(object):
    """
    Class destined for using in a Django-Admin view for generate a report as Excel document.
    Make a features not only an export data of the polls in the text format,
    besides give presentation of the data in charts. For pretty display of the data, used
    a special formaters of the data. As well as used a useful formulas.
    """

    def __init__(self, request, subjects, *args, **kwargs):

        # subjects for a report
        self.subjects = subjects

        # author report
        self.author = request.user.get_full_name()

        # create workbook
        self.workbook = self.get_workbook(request)

        # count row for shift to objects on Excel sheet
        self.objects_shift = 5

        #
        self.all_polls = Poll.objects.prefetch_related('choices', 'votes', 'voteinpoll_set')
        self.all_votes = VoteInPoll.objects.select_related('poll', 'user', 'choice')
        self.all_choices = Choice.objects.select_related('poll')
        self.all_voters = Poll.objects.get_all_voters()
        self.count_polls = self.all_polls.count()
        self.count_choices = Choice.objects.count()
        self.count_votes = self.all_votes.count()

    # Set up document

    def get_workbook(self, request):
        """ """

        # get user
        logger.info('A user {0} demand a report in the Excel about polls'.format(self.author))

        # create in-memory file for writting
        self.output = BytesIO()
        workbook = xlsxwriter.Workbook(self.output)
        logger.debug('Created a workbook for report in the Excel')

        # add properties to document
        logger.critical('A subject of the workbook is not correct')

        list_subjects = ', '.join(subject for subject in self.subjects if subject is not None)
        list_subjects = 'Statistics, {0}'.format(list_subjects)
        workbook.set_properties({
            'title': _('A report about polls'),
            'subject': list_subjects,
            'keywords': _('Polls, choices, votes, voters, results, statistics'),
            'comments': _('Report created with help library XlsxWriter 0.8.7.'),
            'author': self.author,
            'company': settings.SITE_NAME,
        })
        logger.debug('Added properties to the workbook')

        return workbook

    @staticmethod
    def get_filename():
        """Return a name of the file with an extension."""

        return get_filename_with_datetime(Poll._meta.verbose_name, 'xlsx')

    def create_response(self):
        """Create a response with attached a Excel file """

        # create response for Excel
        response = HttpResponse(content_type='application/application/vnd.ms-excel')

        # get filename and attach it to the response
        filename = self.get_filename()
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        logger.debug('Created response for Excel report')
        return response

    def make_report(self):
        """Create a report, on based information, about an exists polls."""

        #
        response = self.create_response()

        self.workbook.add_worksheet(_('Statistics'))
        self.fillup_sheet_statistics()

        # adding needed worksheets and to fill up it
        if 'polls' in self.subjects:
            self.workbook.add_worksheet(_('Polls'))
            self.fillup_sheet_polls()
        if 'choices' in self.subjects:
            self.workbook.add_worksheet(_('Choices'))
            self.fillup_sheet_choices()
        if 'votes' in self.subjects:
            self.workbook.add_worksheet(_('Votes'))
            self.fillup_sheet_votes()
        if 'results' in self.subjects:
            self.workbook.add_worksheet(_('Results'))
            self.fillup_sheet_results()
        if 'voters' in self.subjects:
            self.workbook.add_worksheet(_('Voters'))
            self.fillup_sheet_voters()

        # logger.debug('Added worksheets to the workbook')

        # close the workbook, as well as to write the Excel document in the response and to return it
        self.workbook.close()
        response.write(self.output.getvalue())
        logger.debug('Wrote a PDF in the response')
        logger.info('Succefully created a report about polls in Excel for user {0}'.format(self.author))
        return response

    # Common methods for majority sheets

    @property
    def get_formats(self):
        """Return all styled formats for Excel document as dictionary."""

        return dict(
            title=self.workbook.add_format({
                'bold': True,
                'border': 6,
                'fg_color': '#D7E4BC',
                'align': 'center',
                'valign': 'vcenter',
                'font_size': 30,
            }),
            table_cell_bold=self.workbook.add_format({
                'bg_color': '#F7F7F7',
                'color': 'black',
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
                'bold': True,
            }),
            table_cell_header=self.workbook.add_format({
                'bg_color': '#222222',
                'color': '#ffffff',
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
                'border_color': '#ffff00',
            }),
            table_cell_centered=self.workbook.add_format({
                'border': 1,
                'valign': 'vcenter',
                'align': 'center',
                'text_wrap': True,
                'bg_color': '#F1E8F7',
            }),
            table_cell_datetime=self.workbook.add_format({
                'valign': 'vcenter',
                'align': 'right',
                'border': 1,
                'text_wrap': True,
                'bg_color': '#E5F6E6',
            }),
            table_cell_justify_text=self.workbook.add_format({
                'valign': 'vcenter',
                'align': 'justify',
                'border': 1,
                'text_wrap': True,
                'bg_color': '#E2E4E9',
            }),
            table_cell_title=self.workbook.add_format({
                'bg_color': '#D0B0D9',
                'valign': 'vcenter',
                'align': 'center',
                'border': 2,
                'border_color': '##C4E9ED',
                'text_wrap': True,
                'font_size': 11,
                'bold': True,
            }),
            formula=self.workbook.add_format({
                'border': 2,
                'align': 'right',
                'bg_color': 'yellow',
            }),
            empty_row=self.workbook.add_format({
                'align': 'center',
                'font_color': '#f00000',
                'font_size': 17,
                'bold': True,
                'valign': 'vcenter',
            })
        )

    def write_title(self, title, sheet, count_fields):
        """Write title for passed sheet."""

        title = str(title)

        # since numeration in Excel begin from 0, then a title`s length must be decrement on 1
        title_length = count_fields - 1

        sheet.set_row(1, 80)
        sheet.merge_range(1, 0, 1, title_length, title, self.get_formats['title'])

    def write_field_names(self, field_names, sheet):
        """Write a names of fields of the model Poll, with adding a style format."""

        # all string, marked as translatable, directly convert to string
        # because the Excel does not have a support objects with that type
        sheet.write_row(
            self.objects_shift - 1, 0,
            map(str, field_names),
            self.get_formats['table_cell_header']
        )

        sheet.set_row(self.objects_shift - 1, 40)

    def write_objects(self, sheet, count_fields, empty_msg, qs, func):
        """ """

        sheet.set_row(4, 30)

        if not qs.count():
            count_fields -= 1
            sheet.merge_range(
                self.objects_shift, 0, self.objects_shift, count_fields,
                _(empty_msg),
                self.get_formats['empty_row']
            )
            sheet.set_row(self.objects_shift, 50)
        else:

            # number row for writting information about object
            for num_obj, obj in enumerate(qs):
                num_row = num_obj + self.objects_shift

                # as num_obj is started from 0, than make it +1
                num_obj += 1

                func(sheet, num_row, num_obj, obj)

                # set a height of current row
                self.set_rows_for_sheet_with_objects(sheet, obj, num_row)

    def set_rows_for_sheet_with_objects(self, sheet, obj, num_row):
        """Set a height of rows, on based the Excel 2007 standarts,  """

        # get model
        model = type(obj)

        # choice max count rows in that row and make incrementation it on 1
        all_field_names = model._meta.get_all_field_names()

        # deternimate value of the object with max length
        max_count_rows = 0
        for field_name in all_field_names:
            val = getattr(obj, field_name, '')
            val = str(val)
            count_rows = len(textwrap.wrap(val, 30))
            if max_count_rows < count_rows:
                max_count_rows = count_rows

        # a standart height of a single row is 20, thus make multiplication count_rows on 20
        # for get correct height in Excel
        count_rows = max_count_rows * 20

        sheet.set_row(num_row, count_rows)

    # Filling sheets

    def fillup_sheet_statistics(self):
        """ """

        title = _('Statistics')
        sheet = self.workbook.get_worksheet_by_name('Statistics')

        count_fields = 2

        self.write_title(title, sheet, count_fields)

        sheet.merge_range('A5:B5', _('Common statistics '), self.get_formats['table_cell_title'])
        sheet.write('A6', _('Count polls'), self.get_formats['table_cell_header'])
        sheet.write('B6', self.count_polls, self.get_formats['table_cell_centered'])
        sheet.write('A7', _('Count choices'), self.get_formats['table_cell_header'])
        sheet.write('B7', self.count_choices, self.get_formats['table_cell_centered'])
        sheet.write('A8', _('Count votes'), self.get_formats['table_cell_header'])
        sheet.write('B8', self.count_votes, self.get_formats['table_cell_centered'])
        sheet.write('A9', _('Count voters'), self.get_formats['table_cell_header'])
        sheet.write('B9', self.all_voters.count(), self.get_formats['table_cell_centered'])
        sheet.write('A10', _('Count opened\npolls'), self.get_formats['table_cell_header'])
        sheet.write('B10', Poll.objects.opened_polls().count(), self.get_formats['table_cell_centered'])
        sheet.write('A11', _('Count closed\npolls'), self.get_formats['table_cell_header'])
        sheet.write('B11', Poll.objects.closed_polls().count(), self.get_formats['table_cell_centered'])
        sheet.write('A12', _('Count draft polls'), self.get_formats['table_cell_header'])
        sheet.write('B12', Poll.objects.draft_polls().count(), self.get_formats['table_cell_centered'])
        sheet.write('A13', _('Average count\nchoices in polls'), self.get_formats['table_cell_header'])
        sheet.write('B13', Poll.objects.get_average_count_choices_in_polls(), self.get_formats['table_cell_centered'])
        sheet.write('A14', _('Average count\nvotes in polls'), self.get_formats['table_cell_header'])
        sheet.write('B14', Poll.objects.get_average_count_votes_in_polls(), self.get_formats['table_cell_centered'])

        sheet.merge_range('A16:B16', _('Latest vote'), self.get_formats['table_cell_title'])
        latest_vote = VoteInPoll.objects.get_latest_vote()
        if latest_vote:
            sheet.write('A17', _('User'), self.get_formats['table_cell_header'])
            sheet.write('B17', latest_vote.user.get_full_name(), self.get_formats['table_cell_centered'])
            sheet.write('A18', _('Poll'), self.get_formats['table_cell_header'])
            sheet.write('B18', str(latest_vote.poll), self.get_formats['table_cell_centered'])
            sheet.write('A19', _('Choice'), self.get_formats['table_cell_header'])
            sheet.write('B19', str(latest_vote.choice), self.get_formats['table_cell_justify_text'])
            sheet.write('A20', _('Date voting'), self.get_formats['table_cell_header'])
            sheet.write(
                'B20',
                convert_date_to_django_date_format(latest_vote.date_voting),
                self.get_formats['table_cell_datetime']
            )
        else:
            sheet.merge_range('A17:B20', _('Votes yet not.'), self.get_formats['empty_row'])

        sheet.set_column(0, 1, 20)
        sheet.set_row(4, 40)
        sheet.set_row(9, 40)
        sheet.set_row(10, 40)
        sheet.set_row(11, 40)
        sheet.set_row(12, 40)
        sheet.set_row(13, 40)
        sheet.set_row(15, 40)
        sheet.set_row(16, 60)
        sheet.set_row(17, 60)
        sheet.set_row(18, 60)
        sheet.set_row(19, 40)

    def fillup_sheet_polls(self):
        """ """

        title = _('All polls')
        sheet = self.workbook.get_worksheet_by_name('Polls')
        field_names = [
            '№', _('Id (as UUID)'), _('Title'), _('Slug'),
            _('Description'), _('Count\nvotes'), _('Count\nchoices'),
            _('Status'), _('Latest changed\nof status'), _('Date modified'), _('Date added')
        ]

        count_fields = len(field_names)
        qs = self.all_polls
        func = self.write_poll

        self.write_title(title, sheet, count_fields)
        self.write_field_names(field_names, sheet)
        self.write_objects(sheet, count_fields, 'Polls yet not', qs, func)

        if self.count_polls > 1:
            self.add_formulas_to_polls()
            chart = self.get_chart_polls_by_status()
            sheet.insert_chart('M5', chart)

        # set a width of columns
        sheet.set_column('B1:B1', 15)
        sheet.set_column('C1:D1', 20)
        sheet.set_column('C1:E1', 30)
        sheet.set_column('F1:G1', 8)
        sheet.set_column('I1:K1', 20)

    def fillup_sheet_choices(self):
        """ """

        title = _('All choices')
        sheet = self.workbook.get_worksheet_by_name('Choices')
        field_names = ['№', _('Id (as UUID)'), _('Text of choice'), _('Poll'), _('Count\nvotes')]

        count_fields = len(field_names)
        qs = self.all_choices
        func = self.write_choice

        self.write_title(title, sheet, count_fields)
        self.write_field_names(field_names, sheet)
        self.write_objects(sheet, count_fields, 'Choices yet not', qs, func)

        if self.count_choices > 1:
            self.add_formulas_to_choices()

        # set a width of columns
        sheet.set_column('B1:B1', 15)
        sheet.set_column('C1:C1', 30)
        sheet.set_column('D1:D1', 20)
        sheet.set_column('E1:E1', 10)

    def fillup_sheet_votes(self):
        """ """

        title = _('All votes')
        sheet = self.workbook.get_worksheet_by_name('Votes')
        field_names = ['№', _('Id (as UUID)'), _('Voter'), _('Poll'), _('Choice'), _('Date\nvoting')]

        count_fields = len(field_names)
        qs = self.all_votes
        func = self.write_vote

        self.write_title(title, sheet, count_fields)
        self.write_field_names(field_names, sheet)
        self.write_objects(sheet, count_fields, 'Votes yet not.', qs, func)

        if self.count_votes > 0:
            self.write_count_votes_by_months_for_past_year()
            chart = self.get_chart_votes_for_past_year()
            sheet.insert_chart('H6', chart)

        # set a width of columns
        sheet.set_column('B1:B1', 20)
        sheet.set_column('C1:C1', 20)
        sheet.set_column('D1:E1', 30)
        sheet.set_column('F1:F1', 10)

    def fillup_sheet_results(self):
        """ """

        title = _('Results')
        sheet = self.workbook.get_worksheet_by_name('Results')
        field_names = [_('Count votes'), _('Count choices'), _('Status')]

        count_fields = len(field_names)
        self.write_title(title, sheet, count_fields)

        # if polls yet not
        if not self.count_polls:
            sheet.merge_range('A4:C6', _('Polls yet not'), self.get_formats['empty_row'])
            return

        # if polls already created

        #
        sheet.set_column('A:A', 15)
        sheet.set_column('B:B', 15)
        sheet.set_column('C:C', 60)

        row_len = count_fields - 1

        for i, poll in enumerate(self.all_polls):

            if i == 0:
                num_row = self.objects_shift
            else:
                # num_row = self.objects_shift + 1
                num_row += 5

            # number of row for insert a chart
            start_row = num_row

            sheet.merge_range(
                num_row, 0, num_row, row_len - 1,
                _('Poll with id'),
                self.get_formats['table_cell_bold']
            )
            sheet.write(num_row, row_len, str(poll.pk), self.get_formats['table_cell_centered'])
            sheet.set_row(num_row, 30)

            num_row += 1
            sheet.merge_range(num_row, 0, num_row, row_len, poll.title, self.get_formats['table_cell_title'])
            sheet.set_row(num_row, 40)

            num_row += 1
            sheet.write_row(num_row, 0, field_names, self.get_formats['table_cell_bold'])
            sheet.set_row(num_row, 20)

            num_row += 1
            sheet.write_row(
                num_row, 0,
                [poll.get_count_votes(), poll.get_count_choices(), poll.get_status_display()],
                self.get_formats['table_cell_centered']
            )
            sheet.set_row(num_row, 20)

            num_row += 1
            sheet.merge_range(
                num_row, 0, num_row, row_len,
                _('Choices'),
                self.get_formats['table_cell_bold']
            )
            sheet.set_row(num_row, 40)

            result_poll = poll.get_result_poll()

            num_row += 1
            sheet.write_row(
                num_row, 0,
                ['№', _('Count votes'), _('Choice`s text')],
                self.get_formats['table_cell_bold']
            )
            sheet.set_row(num_row, 20)

            start_data_row = num_row + 2

            if poll.get_count_choices():
                for i, choice_and_count_votes in enumerate(result_poll):
                    num_row += 1
                    choice, count_votes = choice_and_count_votes
                    sheet.write(num_row, 0, i, self.get_formats['table_cell_centered'])
                    sheet.write(num_row, 1, count_votes, self.get_formats['table_cell_centered'])
                    sheet.write(num_row, 2, str(choice), self.get_formats['table_cell_justify_text'])
                    sheet.set_row(num_row, 40)
            else:
                num_row += 1
                sheet.merge_range(num_row, 0, num_row, 2, _('Choices yet not'), self.get_formats['empty_row'])
                sheet.set_row(num_row, 40)

            if poll.get_count_votes():
                chart = self.workbook.add_chart({'type': 'pie'})
                z = num_row + 1
                chart.add_series({
                    'values': '={0}!$B${1}:$B${2}'.format(sheet.name, start_data_row, z),
                    'categories': '={0}!$A${1}:$A${2}'.format(sheet.name, start_data_row, z),
                    'data_labels': {'percentage': True},
                })
                chart.set_title({'name': _('Result of poll')})
                chart.set_style(10)
                sheet.insert_chart('E{0}'.format(start_row), chart)

    def fillup_sheet_voters(self):
        """ """

        title = _('All voters')
        sheet = self.workbook.get_worksheet_by_name('Voters')
        field_names = [
            '№', _('Id (as UUID)'), _('Full name'),
            _('Count votes'), _('Latest vote'), _('Is active\nvoter?'),
            _('All votes')
        ]

        count_fields = len(field_names)
        qs = self.all_voters
        func = self.write_voter

        self.write_title(title, sheet, count_fields)
        self.write_field_names(field_names, sheet)
        self.write_objects(sheet, count_fields, 'Voters yet not.', qs, func)
        # if self.count_votes > 1:
        #     self.add_formulas_to_choices()

        # set a width of columns
        sheet.set_column('B1:B1', 20)
        sheet.set_column('C1:C1', 30)
        sheet.set_column('D1:E1', 15)
        sheet.set_column('F1:F1', 10)
        sheet.set_column('G1:G1', 50)

    # Writting objects

    def write_poll(self, sheet, num_row, num_obj, poll):
        """Write values of fields of objects on passed sheet.
        At the same time set a height of rows, where is wrote an each object."""

        # if polls yet not, write message about that
        # othewise - write polls

        # write values of fields of poll, with adding, where it need, handy to display formats
        sheet.write(num_row, 0, num_obj, self.get_formats['table_cell_centered'])

        # convert UUID to str, because Excel doesn`t have support this type of data
        # and write id as str
        sheet.write(num_row, 1, str(poll.pk), self.get_formats['table_cell_centered'])

        sheet.write(num_row, 2, poll.title, self.get_formats['table_cell_centered'])
        sheet.write(num_row, 3, poll.slug, self.get_formats['table_cell_justify_text'])
        sheet.write(num_row, 4, poll.description, self.get_formats['table_cell_justify_text'])
        sheet.write(num_row, 5, poll.get_count_votes(), self.get_formats['table_cell_centered'])
        sheet.write(num_row, 6, poll.get_count_choices(), self.get_formats['table_cell_centered'])

        # write displayed value of status
        sheet.write(num_row, 7, poll.get_status_display(), self.get_formats['table_cell_centered'])

        # write datatime in django-project datetime format
        sheet.write(
            num_row,
            8,
            convert_date_to_django_date_format(poll.status_changed),
            self.get_formats['table_cell_datetime'])
        sheet.write(
            num_row,
            9,
            convert_date_to_django_date_format(poll.date_modified),
            self.get_formats['table_cell_datetime'])
        sheet.write(
            num_row,
            10,
            convert_date_to_django_date_format(poll.date_added),
            self.get_formats['table_cell_datetime'])

    def write_choice(self, sheet, num_row, num_obj, choice):
        """ """

        # write values of fields of choice, with adding, where it need, handy to display formats
        sheet.write(num_row, 0, num_obj, self.get_formats['table_cell_centered'])

        # convert UUID to str, because Excel doesn`t have support this type of data
        # and write id as str
        sheet.write(num_row, 1, str(choice.pk), self.get_formats['table_cell_centered'])

        sheet.write(num_row, 2, choice.text_choice, self.get_formats['table_cell_justify_text'])
        sheet.write(num_row, 3, str(choice.poll), self.get_formats['table_cell_justify_text'])
        sheet.write(num_row, 4, choice.get_count_votes(), self.get_formats['table_cell_centered'])

    def write_vote(self, sheet, num_row, num_obj, vote):
        """ """

        # write values of fields of vote, with adding, where it need, handy to display formats
        sheet.write(num_row, 0, num_obj, self.get_formats['table_cell_centered'])

        # convert UUID to str, because Excel doesn`t have support this type of data
        # and write id as str
        sheet.write(num_row, 1, str(vote.pk), self.get_formats['table_cell_centered'])

        sheet.write(num_row, 2, vote.user.get_full_name(), self.get_formats['table_cell_justify_text'])
        sheet.write(num_row, 3, str(vote.poll), self.get_formats['table_cell_justify_text'])
        sheet.write(num_row, 4, str(vote.choice), self.get_formats['table_cell_justify_text'])
        sheet.write(
            num_row,
            5,
            convert_date_to_django_date_format(vote.date_voting),
            self.get_formats['table_cell_datetime'],
        )

    def write_voter(self, sheet, num_row, num_obj, voter):
        """ """

        # write values of fields of voter, with adding, where it need, handy to display formats
        sheet.write(num_row, 0, num_obj, self.get_formats['table_cell_centered'])

        # convert UUID to str, because Excel doesn`t have support this type of data
        # and write id as str
        sheet.write(num_row, 1, str(voter.pk), self.get_formats['table_cell_centered'])

        sheet.write(num_row, 2, voter.get_full_name(), self.get_formats['table_cell_centered'])
        sheet.write(num_row, 3, User.polls.get_count_votes(voter), self.get_formats['table_cell_centered'])
        sheet.write(
            num_row, 4,
            convert_date_to_django_date_format(User.polls.get_latest_vote(voter).date_voting),
            self.get_formats['table_cell_datetime'],
        )

        sheet.write(
            num_row, 5,
            Poll.objects.is_active_voter(voter),
            self.get_formats['table_cell_centered'],
        )

        sheet.write(
            num_row, 6,
            User.polls.get_report_votes(voter),
            self.get_formats['table_cell_justify_text'],
        )

    def write_count_votes_by_months_for_past_year(self):
        """ """

        sheet = self.workbook.get_worksheet_by_name('Votes')

        stat = VoteInPoll.objects.get_statistics_count_votes_by_months_for_past_year()

        dates, count_votes = zip(*stat)

        sheet.write('H3', _('Month, year'), self.get_formats['table_cell_bold'])
        sheet.write('H4', _('Count votes'), self.get_formats['table_cell_bold'])
        sheet.merge_range('H2:T2', _('Count votes for the past year'), self.get_formats['title'])
        sheet.set_column('H:H', 20)
        sheet.set_row(2, 30)
        sheet.set_row(3, 30)
        sheet.write_row('I3', dates, self.get_formats['table_cell_centered'])
        sheet.write_row('I4', count_votes, self.get_formats['table_cell_centered'])

    # Add formulas

    def add_formulas_to_choices(self):
        """ """

        sheet = self.workbook.get_worksheet_by_name('Choices')
        count_choices_with_shift = self.count_choices + self.objects_shift
        sheet.write(
            count_choices_with_shift,
            4,
            '=SUM($E$6:$E${0})'.format(count_choices_with_shift),
            self.get_formats['formula'],
        )

    def add_formulas_to_polls(self):
        """Add formulas on a passed sheed."""

        num_row_after_all_objects = self.count_polls + self.objects_shift
        sheet = self.workbook.get_worksheet_by_name('Polls')

        # add formula - Total count votes
        formula_total_count_votes = '=SUM(F6:F%d)' % num_row_after_all_objects
        sheet.write_formula(
            num_row_after_all_objects,
            5,
            formula_total_count_votes,
            self.get_formats['formula'],
        )

        # add formula - Total count choices
        formula_total_count_choices = '=SUM(G6:G%d)' % num_row_after_all_objects
        sheet.write_formula(
            num_row_after_all_objects,
            6,
            formula_total_count_choices,
            self.get_formats['formula'],
        )

    # Charts

    def get_chart_polls_by_status(self):
        """Build, customization and return a chart for display statistics about count votes by a months."""

        # Create chart for display count polls by status, in view barchar
        chart = self.workbook.add_chart({'type': 'column'})
        sheet_statistics = self.workbook.get_worksheet_by_name('Statistics')

        # cutomization of the chart
        chart.set_legend({'none': True})
        chart.set_size({'x_scale': 1.5, 'y_scale': 1.5})
        chart.add_series({
            'values': '={0}!$B$10:$B$12'.format(sheet_statistics.name),
            'categories': '={0}!$A$10:$A$12'.format(sheet_statistics.name),
            'data_labels': {'value': True}
        })
        chart.set_style(37)
        chart.set_x_axis({
            'name': _('Polls by status'),
            'name_font': {
                'bold': True,
                'size': 30,
            },
            'label_position': 'high',
            'num_font': {
                'name': 'Arial',
                'color': 'green',
                'underline': True,
                'bold': True,
            },
        })
        chart.set_plotarea({
            'gradient': {'colors': ['#FFEFD1', '#F0EBD5', '#B69F66']}
        })

        return chart

    def get_chart_votes_for_past_year(self):
        """"""

        chart = self.workbook.add_chart({'type': 'line'})

        sheet = self.workbook.get_worksheet_by_name('Votes')

        # cutomization of the chart
        chart.set_legend({'none': True})
        chart.set_title({
            'layout': {
                'x': 0.3,
                'y': 0.07,
            }
        })
        chart.set_size({'x_scale': 2, 'y_scale': 2})
        chart.add_series({
            'values': '={0}!$I$4:$T$4'.format(sheet.name),
            'categoriesries': '={0}!$I$3:$T$3'.format(sheet.name),
            'marker': {'type': 'square'},
            'data_labels': {'value': True}
        })
        chart.set_style(34)
        chart.set_x_axis({
            'text_axis': True,
            'date_axis': False,
            'name': _('Count votes for the past year'),
            'label_position': 'low',
            'name_font': {
                'size': 14,
                'rotation': 0,
                'bold': True,
            },
            'num_font': {
                'italic': True,
                'rotation': -45,
            },
            'major_gridlines': {
                'visible': True,
                'line': {
                    'width': 1.25,
                    'dash_type': 'dash'
                }
            },
        })
        chart.set_y_axis({
            'name': _('Count votes'),
            'name_font': {
                'size': 14,
                'rotation': -89,
            },
            'name_layout': {
                'x': 0.02,
                'y': 0.3,
            },
            'label_position': 'low',
        })

        return chart


class PollPDFReport(SitePDFReportTemplate):
    """

    """

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(self, *args, **kwargs)
        self.log = self.get_log()
        self.buffer = BytesIO()
        self.doc = self.get_doc()

    def get_log(self):
        """ """

        log = logging.getLogger(__file__)
        terminalHandler = logging.StreamHandler()
        terminalHandler.setLevel(logging.DEBUG)
        log.addHandler(terminalHandler)
        return log

    def add_styles(self):
        """Add styles specific for polls."""

        super(self.__class__, self).add_styles()

        # a style for a table of polls
        # when poll doesn`t have votes at all
        self.ParagraphNoVotes = Paragraph(_('No votes'), self.styles['ItalicCenter'])

        self.PollTableStyle = TableStyle([
            # all cells
            ('GRID', (0, 1), (-1, -1), 0.2, colors.burlywood),
            ('FONTNAME', (0, 0), (-1, -1), 'FreeSans'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTRE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            # fields and table`s title names
            ('FONTNAME', (0, 0), (0, 0), 'FreeSansBold'),
            ('FONTNAME', (0, 1), (0, 1), 'FreeSansBold'),
            ('FONTNAME', (0, 3), (0, 3), 'FreeSansBold'),
            ('FONTNAME', (0, 5), (0, 5), 'FreeSansBold'),
            ('FONTNAME', (0, 7), (0, 7), 'FreeSansBold'),
            ('FONTNAME', (0, 8), (0, 8), 'FreeSansBold'),
            ('FONTNAME', (0, 9), (0, 9), 'FreeSansBold'),
            ('FONTNAME', (0, 10), (0, 10), 'FreeSansBold'),
            ('FONTNAME', (0, 11), (0, 11), 'FreeSansBold'),
            ('FONTNAME', (0, 12), (0, 12), 'FreeSansBold'),
            # span cells
            ('SPAN', (0, 0), (-1, 0)),
            ('SPAN', (0, 1), (-1, 1)),
            ('SPAN', (0, 2), (-1, 2)),
            ('SPAN', (0, 3), (-1, 3)),
            ('SPAN', (0, 4), (-1, 4)),
            ('SPAN', (0, 5), (-1, 5)),
            ('SPAN', (0, 6), (-1, 6)),
            # table`s title
            ('FONTSIZE', (0, 0), (0, 0), 20),
            ('LEADING', (0, 0), (0, 0), 30),
            ('TOPPADDING', (0, 0), (0, 0), 75),
            ('BOTTOMPADDING', (0, 0), (0, 0), 25),
        ])

    def report_polls(self):
        """ """

        # a variable for flovable objects
        story = list()

        # create a response, passing a string as begin of filename
        self.response = self.create_response(Poll._meta.verbose_name_plural)

        # subject the report
        self.subject = 'All about polls'

        # draw statistics about all the polls
        # move on to the suitable page`s template
        story.append(NextPageTemplate('Statistics'))
        story.append(PageBreak())

        # draw table details about all the polls
        tbl = self.get_table_statistics_polls()
        story.append(tbl)

        story.append(NextPageTemplate('Chart'))
        story.append(PageBreak())
        canvas = self.get_canvas_with_piechart_statistics_status_polls()
        story.append(canvas)

        # move on to the suitable page`s template
        story.append(NextPageTemplate('Objects'))
        story.append(PageBreak())

        tbl = self.get_table_all_polls()
        story.append(tbl)

        # build document
        self.doc.build(story)

        # write PDF in response and return it
        self.write_pdf_in_response()
        return self.response

    def report_choices(self):
        """ """

        # a variable for flovable objects
        story = list()

        # create a response, passing a string as begin of filename
        self.response = self.create_response(Choice._meta.verbose_name_plural)

        # subject the report
        self.subject = 'All about choices'

        # draw statistics about all the polls
        # move on to the suitable page`s template
        story.append(NextPageTemplate('Statistics'))
        story.append(PageBreak())

        # draw table details about all the polls
        tbl = self.get_table_statistics_choices()
        story.append(tbl)

        # Draw table all of the choices
        story.append(NextPageTemplate('Objects'))
        story.append(PageBreak())

        tbl = self.get_table_all_choices()
        story.append(tbl)

        # build document
        self.doc.build(story)

        # write PDF in response and return it
        self.write_pdf_in_response()
        return self.response

    def report_votes(self):
        """ """

        # a variable for flovable objects
        story = list()

        # create a response, passing a string as begin of filename
        self.response = self.create_response(_('Votes in polls'))

        # subject the report
        self.subject = 'All about votes'

        # draw statistics about all the polls
        # move on to the suitable page`s template
        story.append(NextPageTemplate('Statistics'))
        story.append(PageBreak())

        # draw table details about all the polls
        tbl = self.get_table_statistics_votes()
        story.append(tbl)

        #
        story.append(NextPageTemplate('Chart'))
        story.append(PageBreak())

        canvas_with_linechart_count_votes_for_past_year = self.get_canvas_with_linechart_count_votes_for_past_year()
        story.append(canvas_with_linechart_count_votes_for_past_year)

        # Draw table of the all choices
        story.append(NextPageTemplate('Objects'))
        story.append(PageBreak())

        tbl = self.get_table_all_votes()
        story.append(tbl)

        # build document
        self.doc.build(story)

        # write PDF in response and return it
        self.write_pdf_in_response()
        return self.response

    def report_polls_results(self):
        """ """

        # a variable for flovable objects
        story = list()

        # create a response, passing a string as begin of filename
        self.response = self.create_response('Results')

        # subject the report
        self.subject = _('Results')

        # move on to page`s template to draw statistics
        story.append(NextPageTemplate('Statistics'))
        story.append(PageBreak())

        # draw statistics about all the polls as table
        tbl = self.get_table_statistics_results_polls()
        story.append(tbl)

        # move on to page`s template to draw tables
        story.append(NextPageTemplate('Objects'))
        story.append(PageBreak())

        # draw tables for polls with low and high activity
        tbl = self.get_table_polls_with_high_activity()
        story.append(tbl)

        story.append(PageBreak())

        tbl = self.get_table_polls_with_low_activity()
        story.append(tbl)

        # draw results all of the polls by PieChart
        # where a each chart will be placed on a separated page
        for poll in Poll.objects.all().prefetch_related('choices', 'voteinpoll_set', 'votes'):

            # move to PageTemplate for draw charts
            story.append(NextPageTemplate('Object'))
            story.append(PageBreak())

            # add detail about poll
            tbl = self.get_table_poll_details(poll)
            story.append(tbl)

            # # move to PageTemplate for draw charts
            story.append(NextPageTemplate('Chart'))
            story.append(PageBreak())

            # # add canvas with result of poll in the form of table
            canvas_chart_result_poll = self.get_canvas_chart_result_poll(poll)
            story.append(canvas_chart_result_poll)

        # build document
        self.doc.build(story)

        # write PDF in response and return it
        self.write_pdf_in_response()
        return self.response

    def get_table_statistics_polls(self):
        """ """

        # if polls not yet, then latest poll will be replace on empty_row
        latest_poll = get_latest_or_none(Poll)
        if latest_poll is not None:
            latest_poll = str(latest_poll)
            latest_poll = '"%s"' % textwrap.fill(latest_poll, 50)

        data = [
            ['Statictics'],
            ['Count the polls', Poll.objects.count()],
            ['Count an opened polls', Poll.objects.opened_polls().count()],
            ['Count a closed polls', Poll.objects.closed_polls().count()],
            ['Count a draft polls', Poll.objects.draft_polls().count()],
            ['Latest an added poll', latest_poll],
            ['Average a count votes in the polls', Poll.objects.get_average_count_votes_in_polls()],
            ['Average a count choices in the polls', Poll.objects.get_average_count_choices_in_polls()],
        ]

        tbl = Table(data, colWidths=[self.doc_width / 1.75, inch], style=self.tblStaticticsStyle)

        return tbl

    def get_table_statistics_choices(self):
        """ """

        data = [
            ['Statictics'],
            ['Count choices', Choice.objects.count()],
        ]
        tbl = Table(data, colWidths=[self.doc_width / 1.75, inch], style=self.tblStaticticsStyle)
        return tbl

    def get_table_statistics_votes(self):
        """ """

        # if votes is exists, then getting atributes of latest vote
        latest_vote = get_latest_or_none(VoteInPoll)
        if latest_vote is not None:
            latest_voter = textwrap.fill(latest_vote.user.get_full_name(), 50)
            latest_date_voting = convert_date_to_django_date_format(latest_vote.date_voting)
            latest_poll = textwrap.fill(str(latest_vote.poll), 50)
            latest_choice = textwrap.fill(str(latest_vote.choice), 50)
        else:
            latest_voter = ''
            latest_date_voting = ''
            latest_poll = ''
            latest_choice = ''

        data = [
            ['Statictics'],
            ['Count a votes', VoteInPoll.objects.count()],
            ['Count a voters', Poll.objects.get_all_voters().count()],
            ['Latest a voter', latest_voter],
            ['Date a latest voting', latest_date_voting],
            ['Poll with the latest vote', latest_poll],
            ['Choice with the latest vote', latest_choice],
        ]

        tbl = Table(data, colWidths=[self.doc_width / 1.75, inch], style=self.tblStaticticsStyle)

        return tbl

    def get_table_statistics_results_polls(self):
        """ """

        # draw table details about all the polls

        # if no votes yet
        try:
            latest_vote = VoteInPoll.objects.latest()
        except VoteInPoll.DoesNotExist:
            latest_date_voting = None
        else:
            latest_date_voting = convert_date_to_django_date_format(latest_vote.date_voting)

        data = [
            ['Statictics'],
            ['Count a polls', Poll.objects.count()],
            ['Count a votes', VoteInPoll.objects.count()],
            ['Count a voters', Poll.objects.get_all_voters().count()],
            ['Date latest voting', latest_date_voting],
        ]

        tbl = Table(data, colWidths=[self.doc_width / 1.75, inch], style=self.tblStaticticsStyle)

        return tbl

    def get_table_all_polls(self):
        """ """

        data = [['Primary\nkey', 'Title', 'Description', 'Status', 'Count\nchoices', 'Count\nvotes', 'Date\nadded']]

        # if objects does not exists yet, then
        # append a whole row with corresponding message
        # else to append objects as rows of table.
        # as well as select corresponding style for table
        if Poll.objects.count():
            style = self.tblObjectsStyle
            for poll in Poll.objects.all().prefetch_related('choices', 'votes', 'voteinpoll_set'):
                row = [
                    textwrap.fill(str(poll.pk), 10),
                    textwrap.fill(poll.title, 20),
                    textwrap.fill(poll.description, 20),
                    poll.get_status_display(),
                    poll.get_count_choices(),
                    poll.get_count_votes(),
                    textwrap.fill(convert_date_to_django_date_format(poll.date_added), 10),
                ]
                data.append(row)
        else:
            style = self.tblSingleEmptyRowStyle
            data.append(['Objects does not exists'])

        tbl = Table(
            data,
            colWidths=[inch / 1.2, inch * 1.5, inch * 1.5, inch / 1.6, inch / 1.8, inch / 1.9, inch / 1.4],
            style=style,
        )

        return tbl

    def get_table_all_votes(self):
        """ """

        data = [[_('Primary\nkey'), _('Poll'), _('Choice'), _('User'), _('Date\nvoting')]]

        # if objects does not exists yet, then
        # append a whole row with corresponding message
        # else to append objects as rows of table.
        # as well as select corresponding style for table
        if VoteInPoll.objects.count():
            style = self.tblObjectsStyle
            for vote in VoteInPoll.objects.select_related('poll', 'user', 'choice'):
                row = [
                    textwrap.fill(str(vote.pk), 10),
                    textwrap.fill(str(vote.poll), 20),
                    textwrap.fill(str(vote.choice), 20),
                    textwrap.fill(vote.user.get_full_name(), 20),
                    textwrap.fill(convert_date_to_django_date_format(vote.date_voting), 10),
                ]
                data.append(row)
        else:
            style = self.tblSingleEmptyRowStyle
            data.append(['Objects does not exists'])

        tbl = Table(
            data,
            colWidths=[inch / 1.2, inch * 1.6, inch * 1.6, inch * 1.5, inch / 1.3],
            style=style,
        )

        return tbl

    def get_table_all_choices(self):
        """ """

        data = [[_('Primary\nkey'), _('Choice`s\ntext'), _('Poll'), _('Count\nvotes')]]

        # if objects does not exists yet, then
        # append a whole row with corresponding message
        # else to append objects as rows of table.
        # as well as select corresponding style for table
        if Choice.objects.count():
            style = self.tblObjectsStyle
            for choice in Choice.objects.select_related('poll').prefetch_related('votes'):
                row = [
                    textwrap.fill(str(choice.pk), 10),
                    textwrap.fill(choice.text_choice, 30),
                    textwrap.fill(str(choice.poll), 30),
                    choice.get_count_votes(),
                ]
                data.append(row)
        else:
            style = self.tblSingleEmptyRowStyle
            data.append(['Objects does not exists'])

        tbl = Table(
            data,
            colWidths=[inch / 1.3, inch * 2.4, inch * 2.4, inch / 1.5],
            style=style,
        )

        return tbl

    def get_table_polls_with_low_activity(self):
        """ """

        qs = Poll.objects.polls_with_low_activity()
        tbl = self._generate_table_polls_by_activity(_('Polls with low activity'), qs)
        return tbl

    def get_table_polls_with_high_activity(self):
        """ """

        qs = Poll.objects.polls_with_high_activity()
        tbl = self._generate_table_polls_by_activity(_('Polls with high activity'), qs)
        return tbl

    def get_canvas_with_piechart_statistics_status_polls(self):
        """ """

        # create canvas for drawing
        canvas = Drawing(self.doc.width, 500)

        #  create chart
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 25
        chart.height = canvas.height - inch * 3
        chart.width = canvas.width - 75
        chart.barSpacing = 1
        chart.barLabelFormat = '%d'
        chart.barLabels.nudge = 10
        chart.valueAxis.labelTextFormat = _('%d polls')
        chart.valueAxis.valueMin = 0

        # add data to the chart
        statistics_polls_by_status = Poll.objects.get_statistics_polls_by_status()
        chart.data = [
            [statistics_polls_by_status['closed']],
            [statistics_polls_by_status['opened']],
            [statistics_polls_by_status['draft']],
        ]

        # create label
        label = Label()
        label.angle = 0
        label.x = canvas.width / 2
        label.y = canvas.height - inch * 1.5
        label.fontSize = 20
        label.fontName = 'FreeSansBold'
        label.setText(_('Count polls by status'))
        label.textAnchor = 'middle'

        # create legend
        legend = Legend()
        legend.colorNamePairs = [
            (colors.red, str(Poll.get_statuses_for_display['closed'])),
            (colors.green, str(Poll.get_statuses_for_display['opened'])),
            (colors.blue, str(Poll.get_statuses_for_display['draft'])),
        ]
        legend.x = canvas.width / 4
        legend.y = 0
        legend.dx = 10
        legend.dy = 10
        legend.alignment = 'right'
        legend.dxTextSpace = 7
        legend.fontName = 'FreeSans'
        legend.fontSize = 17
        legend.columnMaximum = 1

        # add objects to canvas
        canvas.add(chart, 'chart')
        canvas.add(label, 'label')
        canvas.add(legend, 'legend')

        return canvas

    def get_canvas_with_linechart_count_votes_for_past_year(self):
        """ """

        data = VoteInPoll.objects.get_statistics_count_votes_by_months_for_past_year()

        dates, values = zip(*data)

        canvas = Drawing(self.doc.width, self.doc.width)

        chart = HorizontalLineChart()

        valueMin = 0
        valueMax = max(values) + 10

        chart.x = 50
        chart.y = 0
        chart.data = [values]
        chart.fillColor = colors.wheat
        chart.height = canvas.height - inch * 2
        chart.width = canvas.width - 75
        chart.categoryAxis.categoryNames = dates
        chart.categoryAxis.labels.boxAnchor = 'se'
        chart.categoryAxis.labels.angle = 60
        chart.categoryAxis.joinAxisMode = 'bottom'
        chart.valueAxis.valueMin = valueMin
        chart.valueAxis.valueMax = valueMax
        chart.valueAxis.valueStep = self._eval_step_for_valueAxis_linechart(valueMin, valueMax)
        chart.valueAxis.labelTextFormat = _('%d votes ')
        chart.lines[0].strokeWidth = 1
        chart.lines[0].strokeColor = colors.purple
        chart.lines.symbol = makeMarker('Circle')
        chart.lineLabelFormat = '%d'

        label = Label()
        label.x = canvas.width / 2
        label.y = canvas.height - inch * 1.5
        label.setText(_('Count votes for the past year'))
        label.fontName = 'FreeSansBold'
        label.fontSize = 20
        label.textAnchor = 'middle'

        canvas.add(chart)
        canvas.add(label)

        return canvas

    def get_canvas_chart_result_poll(self, poll):
        """ """

        # create canvas place on page
        canvas = Drawing(self.doc.width, 300 + self.doc.topMargin)

        # if poll does not have votes at all
        if not poll.votes.count():
            msg_part1 = String(canvas.width / 6, canvas.height / 2, "Result has not a graphic representation,")
            msg_part1.fillColor = colors.red
            msg_part1.fontName = 'FreeSans'
            msg_part1.fontSize = 18
            msg_part1.text = "Result has not a graphic representation,"
            canvas.add(msg_part1)
            msg_part2 = String(**msg_part1.getProperties())
            msg_part2.text = "because all the choices has not votes."
            msg_part2.y = canvas.height / 2.2
            canvas.add(msg_part2)
            return canvas

        # create pie chart
        chart = Pie()

        # set positions
        chart.x = canvas.width / 4
        chart.y = canvas.height / 6

        # set dimension
        chart.width = 200
        chart.height = 200
        chart.sideLabelsOffset = 0.1

        # add a pointing lines between a slice and its label
        chart.sideLabels = 1

        # get a result of the poll as two-nested list
        # as next: (choice, count votes in that choice)
        result_poll = poll.get_result_poll()

        # make unpack a nested list in a two lists
        # the first - for choices, the second - for count votes in an each choice
        choices, votes = zip(*(result_poll))
        count_choices = len(choices)

        # get names of a unique colors using in ReportLab by passed count
        colors_for_chart = self._get_colors_for_chart(count_choices)

        # get a string representation of the each choice and break it on lines, if need
        choices = (self._textwrap_long_text(str(choice), 60) for choice in choices)

        # make two-nested list as next: (color, object)
        objects_with_colors = tuple(zip(colors_for_chart, choices))

        # add a data to the chart
        data = votes
        logger.debug(data)
        if data == (0, ):
            data = [1, 3, 4, 5, 5]
        chart.data = data

        # add a labels to the chart
        chart.labels = tuple(map(str, data))

        # add a parameters for all slises
        chart.slices.fontName = 'FreeSans'
        chart.slices.fontSize = 15
        chart.slices.strokeWidth = 1
        chart.slices.strokeColor = colors.white
        chart.slices.popout = 0
        chart.slices.labelRadius = 1.25

        # set a color for an each slice
        for i, obj_color in enumerate(objects_with_colors):
            chart.slices[i].fillColor = obj_color[0]

        #
        canvas.add(chart)

        # label for chart
        label = Label()
        label.angle = 0
        label.x = canvas.width / 2
        label.y = canvas.height - inch / 2
        label.fontSize = 20
        label.fontName = 'FreeSansBold'
        label.setText('Result poll')
        label.textAnchor = 'middle'
        canvas.add(label)

        # create legend
        legend = Legend()
        legend.colorNamePairs = objects_with_colors
        legend.x = 0
        legend.y = 0
        legend.dx = 10
        legend.dy = 10
        legend.alignment = 'right'
        legend.deltax = 10
        legend.deltay = 10
        legend.dxTextSpace = 10
        legend.fontName = 'FreeSans'
        legend.fontSize = 14
        legend.columnMaximum = 10

        # set legend
        canvas.add(legend, 'legend')

        return canvas

    def get_table_poll_details(self, poll):
        """ """

        data = []

        # add table`s title
        data.append([_('Poll with primary key\n%s') % poll.pk])

        # add labels of the fields and their values
        data.append([Poll._meta.get_field('title').verbose_name])
        data.append([poll.title])
        data.append([Poll._meta.get_field('slug').verbose_name])
        data.append([poll.slug])
        data.append([Poll._meta.get_field('description').verbose_name])
        data.append([Paragraph(poll.description, self.styles['JustifyParagraph'])])

        # add field "status" with label and value
        # as well as make changes to the styles of table,
        # namely backlight value of field "status"
        data.append([Poll._meta.get_field('status').verbose_name, poll.get_status_display()])
        if poll.status == Poll.CHOICES_STATUS.opened:
            self.PollTableStyle.add('TEXTCOLOR', (1, 7), (1, 7), colors.green)
        elif poll.status == Poll.CHOICES_STATUS.closed:
            self.PollTableStyle.add('TEXTCOLOR', (1, 7), (1, 7), colors.red)
        elif poll.status == Poll.CHOICES_STATUS.draft:
            self.PollTableStyle.add('TEXTCOLOR', (1, 7), (1, 7), colors.blue)

        # add date latest status changing, date modified and date adding
        # with a project`s date/datetime format
        data.append(
            [
                Poll._meta.get_field('status_changed').verbose_name,
                convert_date_to_django_date_format(poll.status_changed),
            ],
        )
        data.append(
            [
                Poll._meta.get_field('date_modified').verbose_name,
                convert_date_to_django_date_format(poll.date_modified),
            ]
        )
        data.append(
            [
                Poll._meta.get_field('date_added').verbose_name,
                convert_date_to_django_date_format(poll.date_added),
            ]
        )

        # add count choices and votes of the poll
        data.append([_('Count votes'), poll.get_count_votes()])
        data.append([_('Count choices'), poll.get_count_choices()])

        # creating and return table
        tbl = Table(data, style=self.PollTableStyle, colWidths=[inch * 3, inch * 3])
        return tbl

    def _get_colors_for_chart(self, count_colors):
        """Return unique color`s names from all default ReportLab`s colors"""

        # get the all reportLab`s colors names as a dictionary {color_name: rgba()}
        dict_colors = colors.getAllNamedColors()

        # remove a bad colors
        dict_colors.pop('white', None)
        dict_colors.pop('black', None)

        # convert the type dict_values to the list
        all_colors = list(dict_colors.values())

        # return a list of a unique colors
        return random.sample(all_colors, count_colors)

    def _textwrap_long_text(self, text, width):
        """ """

        text = textwrap.shorten(text, width * 1.8)
        text = textwrap.fill(text, width)
        return text

    def _generate_table_polls_by_activity(self, header_table, qs):
        """ """

        # two headers to a table
        data_headers = [
            [header_table],
            [_('Poll'), _('Count\nchoices'), _('Count\nvotes'), _('Date last\nvoting'), _('Date added')],
        ]

        # create rows for the table
        data = []
        data.extend(data_headers)

        # if the filtered objects exists, otherwise add an empty_row row after the two headers
        # as well as add style to the table
        if qs.exists():
            style = self.tblFilterObjectsStyle
            for poll in qs.prefetch_related('choices', 'votes', 'voteinpoll_set'):

                # if a poll has votes, then add a details about a latest vote,
                # otherwise add a paragraph with a corresponding message
                date_lastest_voting = poll.get_date_lastest_voting()
                if date_lastest_voting is not None:
                    date_lastest_voting = timezone.localtime(date_lastest_voting)
                    date_lastest_voting = convert_date_to_django_date_format(date_lastest_voting)
                    date_lastest_voting = textwrap.fill(date_lastest_voting, 15)
                else:
                    date_lastest_voting = self.ParagraphNoVotes

                # convert a date added of the poll to a convenient view
                date_added = timezone.localtime(poll.date_added)
                date_added = convert_date_to_django_date_format(date_added)
                date_added = textwrap.fill(date_added, 15)

                # add details about the poll to row
                row = [
                    textwrap.fill(str(poll), 35),
                    poll.get_count_choices(),
                    poll.get_count_votes(),
                    date_lastest_voting,
                    date_added,
                ]
                data.append(row)
        else:
            style = self.tblSingleEmptyRowFilterStyle
            data.append(['Objects does not exists'])

        tbl = Table(
            data,
            colWidths=[inch * 2.6, inch / 1.6, inch / 1.6, inch * 1.2, inch * 1.2],
            style=style,
        )

        return tbl
