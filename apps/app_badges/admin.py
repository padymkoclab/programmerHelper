
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count
from django.contrib import admin

from .models import *


# class UserInline(admin.TabularInline):
#     '''
#         Tabular Inline View for Account
#     '''
#     model = Badge.users.through
#     extra = 1


class BadgeAdmin(admin.ModelAdmin):
    """
    Admin View for Badge
    """

    list_display = ('name', 'short_description', 'get_count_users_with_this_badge', 'date_created')
    list_filter = ['date_created']
    search_fields = ('name', 'short_description')
    fieldsets = (
        (
            Badge._meta.verbose_name, {
                'fields': ['name', 'short_description', 'users'],
            }
        ),
    )
    # inlines = [
    #     UserInline,
    # ]
    readonly_fields = ['users']
    date_hierarchy = 'date_created'

    def get_queryset(self, request):
        qs = super(BadgeAdmin, self).get_queryset(request)
        qs = qs.annotate(count_user_with_this_badge=Count('users'))
        return qs

    def get_count_users_with_this_badge(self, obj):
        return obj.count_user_with_this_badge
    get_count_users_with_this_badge.admin_order_field = 'count_user_with_this_badge'
    get_count_users_with_this_badge.short_description = _('Count users with this badge')


class GettingBadgeAdmin(admin.ModelAdmin):
    '''
    Admin View for GettingBadge
    '''

    list_display = ('badge', 'user', 'date_getting')
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        ('badge', admin.RelatedOnlyFieldListFilter),
        'date_getting',
    )
    date_hierarchy = 'date_getting'
    readonly_fields = ('badge', 'user')
    fieldsets = [
        [
            GettingBadge._meta.verbose_name, {
                'fields': ('badge', 'user'),
            }
        ]
    ]
