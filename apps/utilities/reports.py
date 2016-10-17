
import textwrap
import abc
import io

from django.utils.text import force_text
from django.template.loader import render_to_string
# from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from reportlab.pdfgen import canvas
import xlsxwriter
from weasyprint import HTML as weasyprint_HTML

from utils.django.functions_db import IsNullAsLast

from apps.core.reports import BaseReport

from .models import Category, Utility


class Report(BaseReport):

    theme = _('Utilities')

    def __init__(self, *args, **kwargs):
        self.PDF_class_report = PdfReport
        self.Excel_class_report = ExcelReport

        super().__init__(*args, **kwargs)


class FormatReport(object, metaclass=abc.ABCMeta):

    def __init__(self, *args, **kwargs):
        self.author = kwargs['author']
        self.timezone = kwargs['timezone']
        self.date_created = kwargs['date_created']
        self.location = kwargs['location']
        self.theme = kwargs['theme']
        self.empty_value_display = kwargs['empty_value_display']

    def __call__(self):
        return self.get_output()

    @abc.abstractmethod
    def get_output(self):
        pass


class PdfReport(FormatReport):

    template = 'utilities/admin/utilities.html'

    def get_output(self):

        html_ = render_to_string(self.template, self.context)
        report = weasyprint_HTML(string=html_)
        return report.write_pdf()

    @property
    def context(self):

        utilities = Utility.objects.utilities_with_rating()
        utilities = utilities.annotate(_temp=IsNullAsLast('rating'))
        utilities = utilities.order_by('_temp', '-rating')

        return dict(
            theme=self.theme,
            location=self.location,
            author=self.author,
            date_created=self.date_created,
            timezone=self.timezone,
            empty_value_display=self.empty_value_display,
            categories=Category.objects.categories_with_count_utilities().order_by('-count_utilities'),
            utilities=utilities,
            labels=dict(
                categories=Category._meta.verbose_name_plural,
                category=Category._meta.verbose_name,
                category_count_utilities=Category.get_count_utilities.short_description,
                utilities=Utility._meta.verbose_name_plural,
                utility=Utility._meta.verbose_name,
                utility_rating=_('Rating'),
            )
        )

    def get_output_2(self):
        """ReportLab version."""

        buffer_ = io.BytesIO()
        report = canvas.Canvas(buffer_)
        report.drawString(500, 500, "I made it.")
        report.showPage()
        report.save()

        output = buffer_.getvalue()
        buffer_.close()

        return output


class ExcelReport(FormatReport):

    def get_output(self):

        buffer_ = io.BytesIO()
        self.create_workbook_with_sheets(buffer_)

        self.fill_summary_sheet()
        self.fill_categories_sheet()
        self.fill_utilities_sheet()

        self.workbook.close()

        output = buffer_.getvalue()
        buffer_.close()

        return output

    def create_workbook_with_sheets(self, buffer_):

        workbook = xlsxwriter.Workbook(buffer_)

        workbook.set_properties(dict(
            title=force_text(_('Report')),
            subject=force_text(self.theme),
            author=force_text(self.author),
        ))

        self.worksheets = dict()
        self.worksheets['summary'] = workbook.add_worksheet('Summary')
        self.worksheets['categories'] = workbook.add_worksheet('Categories')
        self.worksheets['utilities'] = workbook.add_worksheet('Utilities')

        # self.worksheets['summary'].activate()
        self.worksheets['utilities'].activate()

        self.workbook = workbook

    def fill_summary_sheet(self):

        worksheet = self.worksheets['summary']
        row_num = 2

        categories = Category.objects.prefetch_related('utilities').iterator()
        for category in categories:
            self.worksheets['summary'].merge_range(
                row_num, 0, row_num, 2, force_text(category), self.formats['category_title']
            )

            self.worksheets['summary'].set_row(row_num, 30)

            if category.utilities.exists():

                utilities = category.utilities.utilities_with_rating()
                utilities = utilities.annotate(_temp=IsNullAsLast('rating'))
                utilities = utilities.order_by('_temp', '-rating')
                utilities = utilities.iterator()

                for i, utility in enumerate(utilities, start=1):

                    row_num += 1

                    worksheet.write(row_num, 0, i, self.formats['center'])

                    utility_display_text = force_text(utility)
                    worksheet.write(row_num, 1, utility_display_text, self.formats['object_display_text'])

                    rating = self.empty_value_display if utility.rating is None else utility.rating
                    worksheet.write(row_num, 2, rating, self.formats['center'])

                    worksheet.set_row(row_num, self.determinate_height_of_row(utility_display_text))
            else:

                row_num += 1

                worksheet.merge_range(
                    row_num, 0, row_num, 2,
                    force_text(_('Category has not utilities')),
                    self.formats['none_utilities']
                )

            row_num += 2

        worksheet.set_column(0, 0, 5)
        worksheet.set_column(1, 1, 50)
        worksheet.set_column(2, 2, 10)

    def fill_categories_sheet(self):

        row_number = 1

        self.worksheets['categories'].write_row(
            row_number, 0,
            (
                '№',
                force_text(_('Category')),
                force_text(_('Count\n utilities')),
            ),
            self.formats['header']
        )
        self.worksheets['categories'].set_row(1, 30)

        categories = Category.objects.categories_with_count_utilities().iterator()
        for i, obj in enumerate(categories, 1):
            row_number += 1
            self.worksheets['categories'].write(row_number, 0, i, self.formats['center'])
            self.worksheets['categories'].write(row_number, 1, force_text(obj))
            self.worksheets['categories'].write(row_number, 2, obj.count_utilities, self.formats['center'])

        self.worksheets['categories'].set_column('A:A', 5)
        self.worksheets['categories'].set_column('B:B', 100)
        self.worksheets['categories'].set_column('C:C', 10)

    def fill_utilities_sheet(self):

        row_number = 1

        self.worksheets['utilities'].write_row(
            row_number, 0,
            (
                '№',
                force_text(_('Utility')),
                force_text(_('Category')),
                force_text(_('Rating')),
            ),
            self.formats['header']
        )
        self.worksheets['utilities'].set_row(1, 30)

        utilities = Utility.objects.select_related('category').utilities_with_rating().iterator()
        for i, utility in enumerate(utilities, 1):

            row_number += 1

            self.worksheets['utilities'].write(row_number, 0, i, self.formats['center'])

            utility_text_display = force_text(utility)
            self.worksheets['utilities'].write(
                row_number, 1, utility_text_display, self.formats['object_display_text']
            )

            category_text_display = force_text(utility.category)
            self.worksheets['utilities'].write(
                row_number, 2, category_text_display, self.formats['object_display_text']
            )

            rating = self.empty_value_display if utility.rating is None else utility.rating
            self.worksheets['utilities'].write(row_number, 3, rating, self.formats['center'])

            self.worksheets['utilities'].set_row(
                row_number,
                self.determinate_height_of_row(utility_text_display, category_text_display)
            )

        self.worksheets['utilities'].set_column('A:A', 5)
        self.worksheets['utilities'].set_column('B:C', 50)
        self.worksheets['utilities'].set_column('D:D', 10)

    @property
    def formats(self):

        formats = dict(
            category_title={
                'bold': True,
                'align': 'center',
                'valign': 'vcenter',
                'text_wrap': True,
                'pattern': 1,
                'font_color': '#ffffff',
                'fg_color': '#222222',
            },
            center={
                'align': 'center',
                'valign': 'vcenter',
            },
            object_display_text={
                'text_wrap': True,
                'align': 'justify',
                'valign': 'vcenter',
            },
            none_utilities={
                'align': 'center',
                'italic': True,
            },
            header={
                'align': 'center',
                'valign': 'vcenter',
                'bold': True,
                'fg_color': '#222222',
                'font_color': '#ffffff',
            },
        )

        return {name: self.workbook.add_format(styles) for name, styles in formats.items()}

    @staticmethod
    def determinate_height_of_row(*texts):
        # work only if width of a column is 50

        count_rows = max(len(textwrap.wrap(text, 50)) for text in texts)
        return count_rows * 15
