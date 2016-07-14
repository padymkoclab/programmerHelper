
from io import BytesIO
import textwrap

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse

import xlsxwriter

from mylabour.utils import get_statistics_count_objects_by_year, get_filename_with_datetime

from .models import Poll, VoteInPoll


# For admin


def make_excel_report_by_object(response, object):
    """Return the response with, filled, in pdf-format, a data about passed the object."""

    raise NotImplementedError


def make_pdf_report_by_object(response, object):
    """Return the response with, filled, in pdf-format, a data about passed the object."""

    raise NotImplementedError


class ExcelReport(object):
    """
    Class destined for using in a Django-Admin view for generate a report as Excel document.
    Make a features not only an export data of the polls in the text format,
    besides give presentation of the data in charts. For pretty display of the data, used
    a special formaters of the data. As well as used a useful formulas.
    """

    def __init__(self, *args, **kwargs):

        # create in-memory file for writting
        self.output = BytesIO()

        # create workbook
        self.workbook = xlsxwriter.Workbook(self.output)

    def get_filename(self):
        """Return a name of the file with an extension."""

        return get_filename_with_datetime(Poll._meta.verbose_name, 'xlsx')

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
            }),
            header=self.workbook.add_format({
                'bg_color': '#F7F7F7',
                'color': 'black',
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
                'bold': True,
            }),
            table=self.workbook.add_format({
                'border': 1,
                'valign': 'vcenter',
                'align': 'center',
            }),
            datetime=self.workbook.add_format({
                'valign': 'vcenter',
                'align': 'right',
                'border': 1,
            }),
            text=self.workbook.add_format({
                'valign': 'vcenter',
                'align': 'justify',
                'border': 1,
                'text_wrap': True,
            }),
            formula=self.workbook.add_format({
                'border': 2,
                'align': 'right',
                'bg_color': 'yellow',
                'border_color': 'green',
            }),
        )

    def write_title(self, sheet):
        """Write title for passed sheet."""

        title_text = 'All polls'
        sheet.merge_range('A2:K3', title_text, self.get_formats['title'])

    def write_field_name(self, sheet):
        """Write a names of fields of the model Poll, with adding a style format."""

        # all string, marked as translatable, directly convert to string
        # because the Excel does not have a support objects with that type
        sheet.write_row(
            'A5',
            map(str, [
                '№',
                _('Id (as UUID)'),
                _('Title'),
                _('Slug'),
                _('Description'),
                _('Count votes'),
                _('Count choices'),
                _('Status'),
                _('Date latest changed of status'),
                _('Date modified'),
                _('Date added'),
            ]),
            self.get_formats['header']
        )

    def write_objects(self, sheet):
        """Write values of fields of objects on passed sheet.
        At the same time set a height of rows, where is wrote an each object."""

        for num_obj, poll in enumerate(Poll.objects.iterator()):

            # number row for writting inforation about object
            num_row = num_obj + 5

            # as num_obj is started from 0, than make it +1
            num_obj += 1

            # write values of fields of poll, with adding, where it need, handy to display formats
            sheet.write(num_row, 0, num_obj, self.get_formats['table'])

            # convert UUID to str, because Excel doesn`t have support this type of data
            # and write id as str
            sheet.write(num_row, 1, str(poll.id), self.get_formats['table'])

            sheet.write(num_row, 2, poll.title, self.get_formats['text'])
            sheet.write(num_row, 3, poll.slug, self.get_formats['text'])
            sheet.write(num_row, 4, poll.description, self.get_formats['text'])
            sheet.write(num_row, 5, poll.get_count_votes(), self.get_formats['table'])
            sheet.write(num_row, 6, poll.get_count_choices(), self.get_formats['table'])

            # write displayed value of status
            sheet.write(num_row, 7, poll.get_status_display(), self.get_formats['table'])

            # write datatime as a string, but in a given format (localizated and timezone)
            sheet.write(num_row, 8, poll.status_changed.strftime('%c %z (%Z)'), self.get_formats['datetime'])
            sheet.write(num_row, 9, poll.date_modified.strftime('%c %z (%Z)'), self.get_formats['datetime'])
            sheet.write(num_row, 10, poll.date_added.strftime('%c %z (%Z)'), self.get_formats['datetime'])

            # set a height of current row
            self.set_rows_for_sheet_with_objects(sheet, poll, num_row)

    def set_rows_for_sheet_with_objects(self, sheet, poll, num_row):
        """Set a height of rows, on based the Excel 2007 standarts,  """

        # choice max count rows in that row and make incrementation it on 1
        count_rows = max(
            textwrap.fill(poll.title, 50).count('\n'),
            textwrap.fill(poll.slug, 50).count('\n'),
            textwrap.fill(poll.description, 50).count('\n'),
        )

        # for correct height of row, make incrementation count rows on 1
        count_rows += 1

        # a standart height of a single row is 20, thus make multiplication count_rows on 20
        # for get correct height in Excel
        count_rows = count_rows * 20
        sheet.set_row(num_row, count_rows)

    def set_columns_for_sheet_with_objects(self, sheet):
        """Set a width of columns, by Excel 2007 standarts, on the sheet, where is wrote the objects."""

        sheet.set_column('B1:B1', 37)
        sheet.set_column('C1:E1', 50)
        sheet.set_column('F1:G1', 15)
        sheet.set_column('I1:K1', 34)

    def add_formulas(self, sheet, num_row_after_all_objects):
        """Add formulas on a passed sheed."""

        # add formula - Total count votes
        formula_total_count_votes = '=SUM(F6:F%d)' % num_row_after_all_objects
        sheet.write_formula(num_row_after_all_objects, 5, formula_total_count_votes, self.get_formats['formula'])

        # add formula - Total count choices
        formula_total_count_choices = '=SUM(G6:G%d)' % num_row_after_all_objects
        sheet.write_formula(num_row_after_all_objects, 6, formula_total_count_choices, self.get_formats['formula'])

    def get_chart_statistics(self):
        """Build, customization and return a chart for display statistics about count votes by a months."""

        # Create chart_statistics_count_votes_by_year on sheet2
        chart_statistics_count_votes_by_year = self.workbook.add_chart({'type': 'line'})

        # make cutomization of chart
        chart_statistics_count_votes_by_year.set_legend({'none': True})
        chart_statistics_count_votes_by_year.set_title({
            'name': str(_('Statistics count votes by year')),
            'layout': {
                'x': 0.3,
                'y': 0.07,
            }
        })
        chart_statistics_count_votes_by_year.set_size({'x_scale': 1.5, 'y_scale': 1.5})
        chart_statistics_count_votes_by_year.set_x_axis({
            'name': str(_('Month, year')),
            'name_font': {
                'size': 13,
                'rotation': 0,
            },
            'num_font': {
                'italic': True,
                'rotation': -45,
            },
            'text_axis': True,
            'major_gridlines': {
                'visible': True,
                'line': {
                    'width': 1.25,
                    'dash_type': 'dash'
                }
            },
        })
        chart_statistics_count_votes_by_year.set_y_axis({
            'name': str(_('Count votes')),
            'name_font': {
                'size': 13,
                'rotation': -89,
            },
            'name_layout': {
                'x': 0.05,
                'y': 0.3,
            }
        })

        return chart_statistics_count_votes_by_year

    def write_data_source_for_chart_statistics(self, sheet):
        """Write a data to sheet of Excel, needed for build the chart statistics."""

        # get a statistics data by votes
        statistics_count_votes_by_year = get_statistics_count_objects_by_year(VoteInPoll, 'date_voting')

        # write data for build chart
        sheet.write_column('A2', list(date for date, count_votes in statistics_count_votes_by_year))
        sheet.write_column('B2', list(count_votes for date, count_votes in statistics_count_votes_by_year))

    def add_series_to_chart_statistics(self, chart, sheet):
        """Add a series data for the chart statistics."""

        # add series to chart
        chart.add_series({
            'categories': [sheet.name, 1, 0, 12, 0],
            'values': [sheet.name, 1, 1, 12, 1],
        })

    def create_response(self):
        """Create a response with attached a Excel file """

        # create response for Excel 2007
        self.response = HttpResponse(content_type='application/application/vnd.ms-excel')

        # get filename and attach it to the response
        filename = self.get_filename()
        self.response['Content-Disposition'] = 'attachment; filename=%s' % filename

    def create_report(self):
        """Create a report, on based information, about an exists polls."""

        #
        self.create_response()

        # create worksheets
        sheet1 = self.workbook.add_worksheet(str(_('Summary')))
        sheet2 = self.workbook.add_worksheet(str(_('Statistics count votes by year')))

        #
        num_row_after_all_objects = Poll.objects.count() + 5

        # working with sheet1
        self.write_title(sheet1)
        self.write_field_name(sheet1)
        self.write_objects(sheet1)
        self.add_formulas(sheet1, num_row_after_all_objects)

        self.set_columns_for_sheet_with_objects(sheet1)

        # # working with sheet2
        sheet2.write('A1', str(_('Month, year')))
        sheet2.write('B1', str(_('Count votes')))
        sheet2.set_column('A:A', 10)
        sheet2.set_column('B:B', 10)

        #
        chart_statistics_count_votes_by_year = self.get_chart_statistics()

        #
        self.write_data_source_for_chart_statistics(sheet2)

        #
        self.add_series_to_chart_statistics(chart_statistics_count_votes_by_year, sheet2)

        # insert the chart in the Excel document
        sheet2.insert_chart('D2', chart_statistics_count_votes_by_year)

        # close the workbook, as well as to write the Excel document in the response and to return it
        self.workbook.close()
        self.response.write(self.output.getvalue())
        return self.response


class PdfReport(object):

    raise NotImplementedError
