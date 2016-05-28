
from django.contrib.contenttypes import admin

from .models import Favour
from .forms import FavourFormSet


class FavourInline(admin.GenericTabularInline):
    '''
        Tabular Inline View for Favour
    '''

    formset = FavourFormSet
    model = Favour
    extra = 0
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
