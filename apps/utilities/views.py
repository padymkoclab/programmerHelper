
from django.views.generic import DetailView

from .models import Category


class CategoryDetailView(DetailView):
    model = Category
    template_name = "utilities/category_detail.html"
