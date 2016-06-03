
from django.contrib.contenttypes import admin as admin_generic
from django.contrib import admin

from .models import Opinion
from .forms import OpinionFormSet


class OpinionInline(admin_generic.GenericTabularInline):
    '''
    Stacked Inline View for Opinion
    '''

    formset = OpinionFormSet
    model = Opinion
    extra = 0
    ct_field = 'content_type'
    ct_fk_field = 'object_id'


class OpinionAdmin(admin.ModelAdmin):
    '''
        Admin View for Comment
    '''

    list_display = ('content_object',)
