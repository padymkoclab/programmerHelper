
from django.contrib.contenttypes import admin

from .models import Reply
from .formsets import ReplyAdminFormSet
from .forms import ReplyAdminModelForm


class ReplyGenericInline(admin.GenericStackedInline):
    '''
    Stacked Inline View for Reply
    '''

    form = ReplyAdminModelForm
    formset = ReplyAdminFormSet
    model = Reply
    extra = 0
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
    fields = (
        'user',
        'text_reply',
        'advantages',
        'disadvantages',
        'mark_for_content',
        'mark_for_style',
        'mark_for_language',
        'get_total_mark',
    )
    readonly_fields = ['get_total_mark']
