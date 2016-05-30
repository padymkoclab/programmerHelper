
from django.contrib.contenttypes import admin

from .models import Reply
from .forms import ReplyFormSet


class ReplyInline(admin.GenericTabularInline):
    '''
    Stacked Inline View for Reply
    '''

    formset = ReplyFormSet
    model = Reply
    extra = 0
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
