
from django.contrib.contenttypes import admin

from .models import Flavour
from .formsets import FlavourFormSet
from .forms import FlavourInlineAdminModelForm


class FlavourGenericInline(admin.GenericTabularInline):
    '''
        Tabular Inline View for Flavour
    '''

    form = FlavourInlineAdminModelForm
    formset = FlavourFormSet
    model = Flavour
    extra = 0
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
    fields = ['user', 'status', 'date_modified', 'date_added']
    readonly_fields = ['date_modified', 'date_added']
