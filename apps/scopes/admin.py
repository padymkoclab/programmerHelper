
from django.contrib.contenttypes import admin as admin_generic
from django.contrib import admin

from .models import Scope
from .forms import ScopeFormSet


class ScopeInline(admin_generic.GenericTabularInline):
    '''
    Stacked Inline View for Scope
    '''

    formset = ScopeFormSet
    model = Scope
    extra = 0
    ct_field = 'content_type'
    ct_fk_field = 'object_id'


class ScopeAdmin(admin.ModelAdmin):
    '''
        Admin View for Scope
    '''

    list_display = ('content_object',)
