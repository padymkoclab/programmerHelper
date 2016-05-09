
from django.views.generic import DetailView

from .models import *


class CourseDetailView(DetailView):
    model = Course
    template_name = "TEMPLATE_NAME"


class LessonDetailView(DetailView):
    model = Lesson
    template_name = "TEMPLATE_NAME"
