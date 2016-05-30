
from django.contrib.contenttypes import admin

from .models import Opinion
from .forms import OpinionFormSet


class OpinionInline(admin.GenericTabularInline):
    '''
    Stacked Inline View for Opinion
    '''

    formset = OpinionFormSet
    model = Opinion
    extra = 0
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
