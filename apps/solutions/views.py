
from django.views.generic import DetailView

from .models import Solution


class SolutionDetailView(DetailView):
    model = Solution
    template_name = "solutions/solution_detail.html"
