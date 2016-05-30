
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView


class ViewPrivacyPolicy(TemplateView):
    """
    Privacy policy page
    """

    template_name = 'privacy_policy/privacy_policy.html'

    def render_to_response(self, context, **response_kwargs):
        context['title_page'] = _('Privacy policy')
        context['template_extend'] = 'project_templates/index.html'
        return super(ViewPrivacyPolicy, self).render_to_response(context, **response_kwargs)
