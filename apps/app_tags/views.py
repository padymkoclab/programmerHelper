
from django.views.generic import DetailView

from .models import Tag


class TagDetailView(DetailView):
    model = Tag
    template_name = "TEMPLATE_NAME"
