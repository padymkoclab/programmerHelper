
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count
from django.contrib import admin

from apps.admin.site import DefaultSiteAdmin
from apps.admin.admin import ModelAdmin, StackedInline, TabularInline
from apps.admin.app import AppAdmin

from .models import Badge, EarnedBadge
from .apps import BadgesConfig


class BadgesAppAdmin(AppAdmin):

    app_config_class = BadgesConfig


# class UserInline(admin.TabularInline):
#     '''
#         Tabular Inline View for Account
#     '''
#     model = Badge.users.through
#     extra = 1


# @admin.register(Badge, site=AdminSite)
class BadgeAdmin(ModelAdmin):
    """
    Admin View for Badge
    """

    list_display = (
        'name', 'category', 'kind', 'description', 'get_count_users', 'date_latest_awarded', 'lastest_awarded_user'
    )
    list_filter = []
    search_fields = ('name', 'description')
    fieldsets = (
        (
            Badge._meta.verbose_name, {
                'fields': ['name', 'description', 'users'],
            }
        ),
    )
    # inlines = [
    #     UserInline,
    # ]
    readonly_fields = ['users']

    def get_queryset(self, request):
        qs = super(BadgeAdmin, self).get_queryset(request)
        qs = qs.annotate(count_user_with_this_badge=Count('users'))
        return qs

    def get_count_users_with_this_badge(self, obj):
        return obj.count_user_with_this_badge
    get_count_users_with_this_badge.admin_order_field = 'count_user_with_this_badge'
    get_count_users_with_this_badge.short_description = _('Count users')


# @admin.register(EarnedBadge, site=AdminSite)
class EarnedBadgeAdmin(ModelAdmin):
    '''
    Admin View for GettingBadge
    '''

    list_display = ('badge', 'user', 'created')
    # list_filter = (
    #     ('user', admin.RelatedOnlyFieldListFilter),
    #     ('badge', admin.RelatedOnlyFieldListFilter),
    #     'created',
    # )
    # date_hierarchy = 'created'
    # readonly_fields = ('badge', 'user')
    # fieldsets = [
    #     [
    #         EarnedBadge._meta.verbose_name, {
    #             'fields': ('badge', 'user',),
    #         }
    #     ]
    # ]


DefaultSiteAdmin.register_app(BadgesAppAdmin)
DefaultSiteAdmin.register_model(Badge, BadgeAdmin)
DefaultSiteAdmin.register_model(EarnedBadge, EarnedBadgeAdmin)
