
from django.views.generic import DetailView

from .models import TestingSuit


class TestingSuitDetailView(DetailView):
    model = TestingSuit
    template_name = "app_testing/test_suit_detail.html"
