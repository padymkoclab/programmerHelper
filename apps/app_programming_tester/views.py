
from django.views.generic import DetailView

from .models import TestSuit


class TestSuitDetailView(DetailView):
    model = TestSuit
    template_name = "app_programming_tester/test_suit_detail.html"
