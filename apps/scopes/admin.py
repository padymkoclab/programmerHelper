
from django.contrib.contenttypes import admin

from .models import Scope
from .forms import ScopeFormSet


class ScopeInline(admin.GenericTabularInline):
    '''
    Stacked Inline View for Scope
    '''

    formset = ScopeFormSet
    model = Scope
    extra = 0
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
