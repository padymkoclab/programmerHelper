
import time

from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.geoip2 import GeoIP2

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Paragraph,
    Table,
    TableStyle,
)

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

from mylabour.utils import (
    get_year_by_slavic_aryan_calendar,
    convert_date_to_django_date_format,
    get_filename_with_datetime,
    get_ip_from_request,
    get_location_from_ip,
)


class SitePDFReportTemplate(object):
    """
    A base class for all all classes generate PDF report on site.
    """
        # register fonts
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    pdfmetrics.registerFont(TTFont('FreeSansBold', 'FreeSansBold.ttf'))

    # def __new__(cls, *args, **kwargs):


        # return super(SitePDFReportTemplate, cls).__new__(cls, *args, **kwargs)

    def __init__(self, request, *args, **kwargs):
        self.now = timezone.now()
        self.styles = getSampleStyleSheet()
        self.slavic_aryan_year = get_year_by_slavic_aryan_calendar(self.now)
        self.request = args[0]

    def get_doc(self):
        """ """

        doc = BaseDocTemplate(
            self.buffer,
            pagesize=A4,
            title=str(_('Report about polls')),
            author='Seti Volkylany',
            showBoundary=False,
        )
        self.doc_width = doc.pagesize[0]
        self.doc_height = doc.pagesize[1]

        # add a page`s template to the document
        self.add_page_templates(doc)

        # add a styles for the entire document
        self.add_styles()

        return doc

    def add_page_templates(self, doc):
        """ """

        frame = Frame(
            doc.leftMargin,
            doc.bottomMargin,
            self.doc_width - doc.rightMargin - doc.leftMargin,
            self.doc_height - doc.topMargin - doc.bottomMargin,
            showBoundary=False,
        )

        doc.addPageTemplates([
            PageTemplate('Title', frames=[frame], onPage=self.title_page),
            PageTemplate('Statistics', frames=[frame], onPage=self.statisctics_page),
            PageTemplate('Objects', frames=[frame], onPage=self.objects_page),
            PageTemplate('Chart', frames=[frame], onPage=self.chart_page),
            PageTemplate('Object', frames=[frame], onPage=self.object_page),
        ])

    def add_styles(self):
        """ """

        self.styles.add(ParagraphStyle(
            'RightParagraph',
            alignment=TA_RIGHT,
            parent=self.styles['Normal'],
            fontName='FreeSans',
            fontSize=16,
        ))
        self.styles.add(ParagraphStyle(
            'JustifyParagraph',
            alignment=TA_JUSTIFY,
            parent=self.styles['Normal'],
            fontName='FreeSans',
            fontSize=14,
            leading=20,
        ))
        self.styles.add(ParagraphStyle(
            'CenterNormal',
            alignment=TA_CENTER,
            parent=self.styles['Normal'],
            fontName='FreeSans',
        ))
        self.styles.add(ParagraphStyle(
            'TitleReport',
            alignment=TA_CENTER,
            fontSize=28,
            fontName='FreeSansBold',
            leading=inch / 2,
        ))
        self.styles.add(ParagraphStyle(
            'ItalicCenter',
            parent=self.styles['Italic'],
            alignment=TA_CENTER,
        ))

        self.tblStaticticsStyle = TableStyle([
            #
            ('SPAN', (0, 0), (1, 0)),
            ('ALIGN', (0, 0), (1, 0), 'CENTRE'),
            ('FONTNAME', (0, 0), (1, 0), 'FreeSansBold'),
            ('FONTSIZE', (0, 0), (1, 0), 25),
            ('TOPPADDING', (0, 0), (1, 0), inch),
            ('BOTTOMPADDING', (0, 0), (1, 0), inch),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.black),
            #
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            ('LINEBELOW', (0, 1), (-1, -1), .2, colors.black),
            ('TOPPADDING', (0, 1), (-1, -1), inch / 5),
            ('FONTNAME', (0, 1), (-1, -1), 'FreeSans'),
        ])

        self.tblObjectsStyle = TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'FreeSansBold'),
            ('FONTNAME', (0, 1), (-1, -1), 'FreeSans'),
            ('GRID', (0, 0), (-1, -1), 0.2, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTRE'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])

        self.tblFilterObjectsStyle = TableStyle([
            ('SPAN', (0, 0), (-1, 0)),
            ('TOPPADDING', (0, 0), (-1, 0), inch / 2),
            ('BACKGROUND', (0, 1), (-1, 1), colors.lightblue),
            ('BOTTOMPADDING', (0, 0), (-1, 0), inch / 2),
            ('FONTSIZE', (0, 0), (-1, 0), 23),
            ('FONTNAME', (0, 0), (-1, 1), 'FreeSansBold'),
            ('FONTNAME', (0, 2), (-1, -1), 'FreeSans'),
            ('GRID', (0, 1), (-1, -1), 0.2, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTRE'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])

    def create_response(self, begin_filename):
        """Create and to return a HttpResponse with attached a pdf-file."""

        # create a response
        response = HttpResponse(content_type='application/pdf')

        # get a filename with an extension
        filename = get_filename_with_datetime(begin_filename, 'pdf')

        # attach file to the response and return it
        response['Content-Disposition'] = 'atachment; filename=%s' % filename
        return response

    def write_pdf_in_response(self):
        """Write the generated PDF data in the response."""

        # get the value of the BytesIO buffer and write it to the response.
        pdf = self.buffer.getvalue()
        self.buffer.close()
        self.response.write(pdf)

    def title_page(self, canv, doc):
        """ """

        canv.saveState()

        header = Paragraph('ProgrammerHelper.com', self.styles['CenterNormal'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canv, doc.leftMargin, self.doc_height - self.doc.topMargin)

        footer = Paragraph(
            '{0} A. D. ({1} от СМЗХ)'.format(self.now.year, self.slavic_aryan_year),
            self.styles['CenterNormal']
        )
        footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canv, doc.leftMargin, inch / 2)

        title = Paragraph(_('Report on subject'), self.styles['TitleReport'])
        title.wrap(doc.width, doc.height)
        title.drawOn(canv, doc.leftMargin, self.doc_height / 1.6)

        subject = Paragraph('\"%s\"' % self.subject, self.styles['TitleReport'])
        subject.wrap(doc.width, doc.height)
        subject.drawOn(canv, doc.leftMargin, self.doc_height / 1.8)

        # get an IP-address from the request
        ip = get_ip_from_request(self.request)

        # get details about a location, from the IP-address
        GeoLocation = get_location_from_ip(ip)

        location = Paragraph(
            _('Location: {0}, {1}').format(GeoLocation['city'], GeoLocation['country_name']),
            self.styles['RightParagraph']
        )
        location.wrap(doc.width, doc.height)
        location.drawOn(canv, self.doc.leftMargin, self.doc.bottomMargin + inch * 2)

        user_full_name = self.request.user.get_full_name()
        author = Paragraph(_('Author: %s') % user_full_name, self.styles['RightParagraph'])
        author.wrap(doc.width, doc.height)
        author.drawOn(canv, self.doc.leftMargin, self.doc.bottomMargin + inch * 1.5)

        date_generation = Paragraph(
            _('Generated: %s') % convert_date_to_django_date_format(self.now),
            self.styles['RightParagraph']
        )
        date_generation.wrap(doc.width, doc.height)
        date_generation.drawOn(canv, self.doc.leftMargin, self.doc.bottomMargin + inch)

        offset_hours = -time.timezone / 3600

        current_timezone = Paragraph(
            _('Timezone: {0} ({1:+} hour/s to UTC)').format(settings.TIME_ZONE, offset_hours),
            self.styles['RightParagraph']
        )
        current_timezone.wrap(doc.width, doc.height)
        current_timezone.drawOn(canv, self.doc.leftMargin, self.doc.bottomMargin + inch / 2)

        canv.restoreState()

    def statisctics_page(self, canv, doc):
        """ """

        canv.saveState()

        self._draw_header_and_footer_later_pages(canv, doc, 'Statistics')

        canv.restoreState()

    def objects_page(self, canv, doc):
        """ """

        canv.saveState()

        self._draw_header_and_footer_later_pages(canv, doc, 'Objects')

        canv.restoreState()

    def chart_page(self, canv, doc):
        """ """

        canv.saveState()

        self._draw_header_and_footer_later_pages(canv, doc, 'Chart')

        canv.restoreState()

    def object_page(self, canv, doc):
        """ """

        canv.saveState()

        self._draw_header_and_footer_later_pages(canv, doc, 'Object')

        canv.restoreState()

    def _draw_header_and_footer_later_pages(self, canv, doc, text_right_header):
        """ """

        data = [['%s' % self.subject, text_right_header]]
        tblStyle = TableStyle([
            ('LINEBELOW', (0, 0), (-1, -1), .2, colors.black),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('FONTNAME', (1, 0), (1, 0), 'FreeSansBold'),
        ])
        colWidth = (self.doc_width - doc.leftMargin - doc.rightMargin) / 2
        tbl = Table(data, colWidths=[colWidth, colWidth], style=tblStyle)
        w, h = tbl.wrap(self.doc_width, self.doc_height)
        tbl.drawOn(canv, doc.leftMargin, self.doc_height - doc.topMargin)

        canv.drawCentredString(self.doc_width / 2, self.doc.bottomMargin - 15, 'Page %s' % str(doc.page))
