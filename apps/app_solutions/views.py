
from django.views.generic import DetailView

from .models import SolutionCategory, Solution


class SolutionCategoryDetailView(DetailView):
    model = SolutionCategory
    template_name = "TEMPLATE_NAME"


class SolutionDetailView(DetailView):
    model = Solution
    template_name = "TEMPLATE_NAME"
