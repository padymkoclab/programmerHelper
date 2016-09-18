
from django.contrib.contenttypes import admin as admin_generic
from django.contrib import admin

from .models import Mark
from .formsets import MarkAdminFormSet
from .forms import MarkAdminModelForm


class MarkGenericInline(admin_generic.GenericTabularInline):
    '''
    Stacked Inline View for Mark
    '''

    form = MarkAdminModelForm
    formset = MarkAdminFormSet
    model = Mark
    extra = 0
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
    fiedls = ('user', 'mark', 'date_modified', 'date_added')
    readonly_fields = ('date_modified', 'date_added')

    suit_classes = 'suit-tab suit-tab-marks'


class MarkAdmin(admin.ModelAdmin):
    '''
        Admin View for Mark
    '''

    list_display = ('content_object',)
