
from django.views.generic import DetailView, ListView

from .models import Newsletter


class NewsletterDetailView(DetailView):
    model = Newsletter
    template_name = "TEMPLATE_NAME"


class NewslettersListView(ListView):
    model = Newsletter
    template_name = "TEMPLATE_NAME"
