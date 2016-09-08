
from django.views.generic import DetailView

from .models import Category, Solution


class CategoryDetailView(DetailView):
    model = Category
    template_name = "solutions/category_detail.html"


class SolutionDetailView(DetailView):
    model = Solution
    template_name = "solutions/solution_detail.html"
