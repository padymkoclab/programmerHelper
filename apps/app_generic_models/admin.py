
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
# from django.db.models import Count
# from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from .models import UserComment_Generic, UserLike_Generic, UserOpinion_Generic


class UserComment_GenericAdmin(admin.ModelAdmin):
    '''
        Admin View for UserComment_Generic
    '''

    list_display = ('content_object', 'content_type', 'author', 'is_new', 'date_modified', 'date_added')
    list_filter = (
        ('content_type', admin.RelatedOnlyFieldListFilter),
        ('author', admin.RelatedOnlyFieldListFilter),
        'date_modified',
        'date_added',
    )
    date_hierarchy = 'date_modified'
    fields = ['author', 'content_type', 'text_comment', 'object_id']
    search_fields = ('content_object',)


class UserOpinion_GenericAdmin(admin.ModelAdmin):
    '''
        Admin View for UserOpinion_Generic
    '''

    list_display = (
        'content_object',
        'content_type',
        'user',
        'is_useful',
        'display_is_favorite_as_boolean',
        'is_new',
        'date_modified',
    )
    list_filter = (
        ('content_type', admin.RelatedOnlyFieldListFilter),
        ('user', admin.RelatedOnlyFieldListFilter),
        'is_useful',
        'is_favorite',
        'date_modified',
    )
    date_hierarchy = 'date_modified'
    fields = ['content_type', 'object_id', 'user', 'is_useful', 'is_favorite']
    search_fields = ('content_object',)


class UserLike_GenericAdmin(admin.ModelAdmin):
    '''
        Admin View for UserLike_Generic
    '''

    list_display = (
        'content_object',
        'content_type',
        'user',
        'liked_it',
        'is_new',
        'date_modified',
    )
    list_filter = (
        ('content_type', admin.RelatedOnlyFieldListFilter),
        ('user', admin.RelatedOnlyFieldListFilter),
        'liked_it',
        'date_modified',
    )
    date_hierarchy = 'date_modified'
    fields = ['content_type', 'object_id', 'user', 'liked_it']
    search_fields = ('content_object',)


class OpinionGenericInline(GenericTabularInline):
    model = UserOpinion_Generic
    extra = 1
    fields = ['user', 'is_useful', 'is_favorite']


class CommentGenericInline(GenericStackedInline):
    model = UserComment_Generic
    extra = 1
    fields = ['author', 'text_comment']


class LikeGenericInline(GenericTabularInline):
    model = UserLike_Generic
    extra = 1
    fields = ['user', 'liked_it']
