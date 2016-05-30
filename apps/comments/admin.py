
from django.contrib.contenttypes import admin

from .models import Comment


class CommentInline(admin.GenericStackedInline):
    '''
    Stacked Inline View for Comment
    '''

    model = Comment
    extra = 0
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
    template = 'comments/stacked.html'
