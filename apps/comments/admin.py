
from django.contrib.contenttypes import admin as admin_generic

from apps.admin.admin import ModelAdmin, TabularInline
from apps.admin.app import AppAdmin
from apps.admin.utils import register_app, register_model

from .apps import CommentsConfig
from .models import Comment
from .forms import CommentInlineAdminModelForm


@register_app
class CommentAppAdmin(AppAdmin):

    app_config_class = CommentsConfig


class CommentGenericInline(admin_generic.GenericStackedInline):
    '''
    Stacked Inline View for Comment
    '''

    form = CommentInlineAdminModelForm
    model = Comment
    extra = 0
    ct_field = 'content_type'
    ct_fk_field = 'object_id'

    readonly_fields = ['rating', 'updated', 'created']

    def get_fields(self, request, obj=None):

        fields = ['user', 'text_comment', 'rating', 'updated', 'created']

        return fields


@register_model(Comment)
class CommentAdmin(ModelAdmin):
    '''
        Admin View for Comment
    '''

    list_display = ('user', 'is_new', 'content_type', 'updated', 'created')
    # list_display = ('content_object', 'user', 'content_type', 'rating', 'is_new', 'updated', 'created')
    # list_filter = ('',)
    # search_fields = ('',)

    # def get_list_display(self, request):
    #     return super(CommentAdmin, self).get_list_display(request)
