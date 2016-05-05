
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from .views import ViewPrivacyPolicy


class Test_ViewPrivacyPolicy(TestCase):
    """
    Testing view ViewPrivacyPolicy of application "app_privacy_policy"
    """

    def setUp(self):
        factory = RequestFactory()
        url = reverse('app_privacy_policy:privacy_policy')
        self.request = factory.get(url)

    def test_render_view(self):
        response = ViewPrivacyPolicy.as_view()(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('app_privacy_policy/privacy_policy.html', response.template_name)
        self.assertEqual(response.context_data['title_page'], 'Privacy policy')
        self.assertEqual(response.context_data['template_extend'], 'project_templates/index.html')
