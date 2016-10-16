
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
        utilities = utilities.annotate(rating_with_null=IsNullAsLast('rating'))
        utilities = utilities.order_by('rating_with_null', '-rating')

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
        workbook = xlsxwriter.Workbook(buffer_)

        workbook.set_properties(dict(
            title=force_text(_('Report')),
            subject=force_text(self.theme),
            author=force_text(self.author),
        ))

        self.worksheet_categories = workbook.add_worksheet('Categories')
        self.worksheet_utilities = workbook.add_worksheet('Utilities')
        self.worksheet_summary = workbook.add_worksheet('Summary')

        categories = Category.objects.categories_with_count_utilities()
        utilities = Utility.objects.utilities_with_rating()

        bold = workbook.add_format({'bold': True})

        self.worksheet_categories.write_row(
            1, 0,
            (
                '№',
                force_text(_('Category')),
                force_text(_('Count utilities')),
            )
        )
        self.worksheet_categories.set_row(1, 20, bold)
        for i, obj in enumerate(categories):
            i += 2
            self.worksheet_categories.write_number(i, 0, i)
            self.worksheet_categories.write(i, 1, force_text(obj))
            self.worksheet_categories.write(i, 2, obj.count_utilities)
        else:
            self.worksheet_categories.write_number(i + 1, 0, i)
            self.worksheet_categories.set_column('A:A', 5)
            self.worksheet_categories.set_column('B:B', 100)
            self.worksheet_categories.set_column('C:C', 10)

        self.worksheet_utilities.write_row(
            1, 0,
            (
                '№',
                force_text(_('Utility')),
                force_text(_('Category')),
                force_text(_('Rating')),
            )
        )
        self.worksheet_utilities.set_row(1, 20, bold)
        for i, obj in enumerate(utilities):
            i += 2
            self.worksheet_utilities.write_number(i, 0, i)
            self.worksheet_utilities.write(i, 1, force_text(obj))
            self.worksheet_utilities.write(i, 2, force_text(obj.category))
            self.worksheet_utilities.write(i, 3, obj.rating)
        else:
            self.worksheet_utilities.write_number(i + 1, 0, i)
            self.worksheet_utilities.set_column('A:A', 5)
            self.worksheet_utilities.set_column('B:C', 100)
            self.worksheet_utilities.set_column('D:D', 10)

        workbook.close()

        output = buffer_.getvalue()
        buffer_.close()

        return output
