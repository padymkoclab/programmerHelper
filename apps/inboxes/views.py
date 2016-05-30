
from django.views.generic import DetailView

from .models import Inbox


class InboxDetailView(DetailView):
    model = Inbox
    template_name = "TEMPLATE_NAME"
