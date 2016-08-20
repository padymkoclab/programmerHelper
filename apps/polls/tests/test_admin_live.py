
# import io

# import openpyxl

# from mylabour.test_utils import EnhancedTestCase

# from config.admin import AdminSite

# from apps.polls.models import Poll
# from apps.polls.admin import PollAdmin


# class Tests(EnhancedTestCase):

#     @classmethod
#     def setUpTestData(cls):
#         cls.call_command('factory_test_users', '1')
#         cls.active_superuser = cls.django_user_model.objects.first()
#         cls._make_user_as_active_superuser(cls.active_superuser)

#         cls.PollAdmin = PollAdmin(Poll, AdminSite)

#     def setUp(self):
#         self.buffer = io.BytesIO()

#     def _make_request_and_return_excelfile(self, data):
#         request = self.factory.post('admin:polls_make_report', data)
#         request.user = self.active_superuser
#         response = self.PollAdmin.view_make_report(request)
#         return openpyxl.load_workbook(io.BytesIO(response))

#     def test_(self):

#         data = {
#             'output_report': 'report_excel',
#             'polls': 'polls',
#             'choices': 'choices',
#             'votes': 'votes',
#             'voters': 'voters',
#             'results': 'results',
#         }

#         excelfile = self._make_request_and_return_excelfile(data)
#         import ipdb; ipdb.set_trace()
