
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count
from django.contrib import admin

from .models import *


class UserInline(admin.TabularInline):
    '''
        Tabular Inline View for Account
    '''
    model = Badge.users.through
    extra = 1


class BadgeAdmin(admin.ModelAdmin):
    """
    Admin View for Badge
    """

    list_display = ('name', 'short_description', 'get_count_users_with_this_badge', 'date_created')
    list_filter = ['date_created']
    search_fields = ('name', 'short_description')
    fieldsets = (
        (
            None, {
                'fields': ['name', 'short_description'],
            }
        ),
    )
    inlines = [
        UserInline,
    ]
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

    list_display = ('badge', 'account', 'date_getting')
    list_filter = (
        ('account', admin.RelatedFieldListFilter),
        ('badge', admin.RelatedFieldListFilter),
        'date_getting',
    )
    date_hierarchy = 'date_getting'
