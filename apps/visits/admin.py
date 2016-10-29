
from django.utils.translation import ugettext_lazy as _

from apps.admin.admin import ModelAdmin
from apps.admin.app import AppAdmin
from apps.admin.utils import register_app, register_model

from .models import Attendance
from .apps import VisitsConfig


@register_app
class VisitsAppAdmin(AppAdmin):

    app_config_class = VisitsConfig


@register_model(Attendance)
class Attendance(ModelAdmin):

    list_display = ('date', 'get_count_visitors')
