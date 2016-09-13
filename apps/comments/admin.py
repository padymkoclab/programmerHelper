
from django.contrib.contenttypes import admin as admin_generic
from django.contrib import admin

from .models import Comment
from .forms import CommentInlineAdminModelForm


class CommentGenericInline(admin_generic.GenericStackedInline):
    '''
    Stacked Inline View for Comment
    '''

    form = CommentInlineAdminModelForm
    model = Comment
    extra = 0
    ct_field = 'content_type'
    ct_fk_field = 'object_id'

    readonly_fields = ['rating', 'date_modified', 'date_added']

    def get_fields(self, request, obj=None):

        fields = ['user', 'text_comment', 'rating', 'date_modified', 'date_added']

        return fields


class CommentAdmin(admin.ModelAdmin):
    '''
        Admin View for Comment
    '''

    list_display = ('content_object', 'user', 'content_type', 'rating', 'is_new', 'date_modified', 'date_added')
    # list_filter = ('',)
    # search_fields = ('',)

    def get_list_display(self, request):
        return super(CommentAdmin, self).get_list_display(request)
