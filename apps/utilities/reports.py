
import io

from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from reportlab.pdfgen import canvas
import xlsxwriter
from weasyprint import HTML as weasyprint_HTML

from utils.python.utils import get_filename_with_datetime

from apps.core.reports import BaseReport

from .models import Category, Utility


class Report(BaseReport):

    template = 'utilities/admin/utilities.html'

    RESPONSE_DETAILS = {
        'pdf': {
            'content_type': 'application/pdf',
            'extension': 'pdf',
        },
        'excel': {
            'content_type': 'application/vnd.ms-excel',
            'extension': 'xlsx',
        },
    }

    def __init__(self, report_type, filename):
        self.type = report_type
        self.filename = filename

    def __call__(self):
        return self.generate_report()

    def generate_report(self):

        response = self.get_response()

        if self.type == 'pdf':
            output = self.pdf_output()
            output = self.pdf_report_template()
        elif self.type == 'excel':
            output = self.excel_output()

        response.write(output)

        return response

    def get_response(self):

        response_details = self.RESPONSE_DETAILS[self.type]
        response = HttpResponse(content_type=response_details['content_type'])
        filename = get_filename_with_datetime(self.filename, response_details['extension'])
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response

    def pdf_output(self):

        buffer_ = io.BytesIO()
        report = canvas.Canvas(buffer_)
        report.drawString(500, 500, "I made it.")
        report.showPage()
        report.save()

        output = buffer_.getvalue()
        buffer_.close()

        return output

    def excel_output(self):

        buffer_ = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer_)
        worksheet = workbook.add_worksheet()

        worksheet.write('A1', 'I made it')

        workbook.close()

        output = buffer_.getvalue()
        buffer_.close()

        return output

    def pdf_report_template(self):

        html_ = render_to_string(
            self.template,
            dict(
                empty_value_display=self.empty_value_display,
                categories=Category.objects.categories_with_count_utilities().order_by('-count_utilities'),
                utilities=Utility.objects.utilities_with_rating().order_by('-rating'),
                labels=dict(
                    categories=Category._meta.verbose_name_plural,
                    category=Category._meta.verbose_name,
                    category_count_utilities=Category.get_count_utilities.short_description,
                    utilities=Utility._meta.verbose_name_plural,
                    utility=Utility._meta.verbose_name,
                    utility_rating=_('Rating'),
                )
            )
        )
        report = weasyprint_HTML(string=html_)
        return report.write_pdf()
