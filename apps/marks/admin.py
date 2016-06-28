
from django.contrib.contenttypes import admin as admin_generic
from django.contrib import admin

from .models import Mark
from .forms import MarkFormSet


class MarkInline(admin_generic.GenericTabularInline):
    '''
    Stacked Inline View for Mark
    '''

    formset = MarkFormSet
    model = Mark
    extra = 0
    ct_field = 'content_type'
    ct_fk_field = 'object_id'


class MarkAdmin(admin.ModelAdmin):
    '''
        Admin View for Mark
    '''

    list_display = ('content_object',)
