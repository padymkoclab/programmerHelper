
from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.admin.forms import AddModelForm

from utils.django.widgets import AutosizedTextarea

from .models import Category, Utility


class CategoryAdminModelForm(AddModelForm):

    disabled_fields = ('slug', )

    class Meta:
        widgets = {
            'description': AutosizedTextarea(),
        }


class UtilityAdminModelForm(AddModelForm):

    class Meta:
        widgets = {
            'description': AutosizedTextarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].widget.widget.attrs['class'] = 'span11'
