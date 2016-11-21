
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured


# Origin from the "Two spoons of Django", page 129
class ActionMixin(object):
    """

    """

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.requet, self.success_msg)
        return super(ActionMixin, self).form_valid(form)


class ContextTitleMixin:
    """

    """

    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # if self.title is None:

        #     raise ImproperlyConfigured(
        #         '{} require a definition of an attribute "title"'.format(type(self))
        #     )

        context['title'] = self.title

        return context
