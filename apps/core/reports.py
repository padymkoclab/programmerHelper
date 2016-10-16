
import logging
import socket

from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.contrib.gis.geoip2 import GeoIP2

from utils.python.utils import get_filename_with_datetime
from utils.django.utils import get_output_from_DTL


logger = logging.getLogger('django.development')


class BaseReport(object):

    PDF_class_report = None
    Excel_class_report = None
    empty_value_display = '-'

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

    logger = logger

    def __init__(self, request, report_type, filename):
        self.request = request
        self.type = report_type
        self.filename = filename

    def __call__(self):
        return self.generate_report()

    @property
    def report_attributes(self):
        return dict(
            location=self.get_location(),
            author=self.get_author(),
            theme=self.theme,
            timezone=self.get_timezone(),
            date_created=self.get_date_created(),
            empty_value_display=self.empty_value_display,
        )

    def generate_report(self):

        response = self.get_response()

        if self.type == 'pdf':
            report_class = self.PDF_class_report
        elif self.type == 'excel':
            report_class = self.Excel_class_report

        report = report_class(**self.report_attributes)
        output = report()

        response.write(output)

        return response

    def get_response(self):

        response_details = self.RESPONSE_DETAILS[self.type]
        response = HttpResponse(content_type=response_details['content_type'])
        filename = get_filename_with_datetime(self.filename, response_details['extension'])
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response

    def get_location(self):
        geo_ip = GeoIP2()
        try:
            location = geo_ip.city(self.request.get_host())
        except socket.gaierror:
            logger.error('Could not determinate a location of user')
            return _('Unknown')
        else:
            return '{0[city]}, {0[country_name]}'.format(location)

    def get_author(self):

        return self.request.user.get_full_name()

    def get_timezone(self):
        timezone_name = get_output_from_DTL("{% now 'T' %}")
        offset = get_output_from_DTL("{% now 'O' %}")

        if len(offset) == 4:
            sign, hours, minutes = '', offset[1:3], offset[3:]
        elif len(offset) == 5:
            sign, hours, minutes = offset[0], offset[1:3], offset[3:]

        hours = hours[1] if hours.startswith('0') else hours

        return '{} {}{}:{}'.format(timezone_name, sign, hours, minutes)

    def get_date_created(self):

        return get_output_from_DTL("{% now 'DATETIME_FORMAT' %}")
