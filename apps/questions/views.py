
from django.views.generic import DetailView

from .models import Question


class QuestionDetailView(DetailView):
    model = Question
    template_name = "TEMPLATE_NAME"
