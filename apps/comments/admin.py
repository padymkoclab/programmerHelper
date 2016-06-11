
from django.contrib.contenttypes import admin as admin_generic
from django.contrib import admin

from .models import Comment


class CommentInline(admin_generic.GenericStackedInline):
    '''
    Stacked Inline View for Comment
    '''

    model = Comment
    extra = 0
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
    template = 'comments/stacked.html'


class CommentAdmin(admin.ModelAdmin):
    '''
        Admin View for Comment
    '''

    list_display = ('content_object', 'account', 'content_type', 'rating', 'is_new', 'date_modified', 'date_added')
    # list_filter = ('',)
    # search_fields = ('',)

    def get_list_display(self, request):
        return super(CommentAdmin, self).get_list_display(request)
