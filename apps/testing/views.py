
from django.views.generic import DetailView

from .models import Suit


class SuitDetailView(DetailView):
    model = Suit
    template_name = "testing/suit_detail.html"
