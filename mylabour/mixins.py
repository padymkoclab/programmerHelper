
from django.contrib import messages


# Origin "Two spoons of Django", page 129
class ActionMixin(object):
    """

    """

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.requet, self.success_msg)
        return super(ActionMixin, self).form_valid(form)
