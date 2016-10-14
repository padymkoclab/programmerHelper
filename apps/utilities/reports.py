
from django.http import HttpResponse


class Report(object):

    def __init__(self, report_type):
        self.type = report_type

    def __call__(self):
        return self.generate_report()

    def generate_report(self):
        return HttpResponse()
