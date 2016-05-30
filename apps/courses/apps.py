
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class CoursesConfig(AppConfig):
    name = "apps.courses"
    verbose_name = _("Courses")
