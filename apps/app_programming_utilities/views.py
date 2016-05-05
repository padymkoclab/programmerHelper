
from django.views.generic import DetailView

from .models import ProgrammingCategory


class ProgrammingCategoryDetailView(DetailView):
    model = ProgrammingCategory
    template_name = "TEMPLATE_NAME"
