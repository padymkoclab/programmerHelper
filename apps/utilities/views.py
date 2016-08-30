
from django.views.generic import DetailView

from .models import UtilityCategory


class UtilityCategoryDetailView(DetailView):
    model = UtilityCategory
    template_name = "utilities/category_detail.html"
