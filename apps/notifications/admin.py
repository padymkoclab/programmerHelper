
from django.utils.html import format_html
from django.contrib import admin

from apps.core.admin import AdminSite

from .models import Notification


@admin.register(Notification, site=AdminSite)
class NotificationAdmin(admin.ModelAdmin):
    '''
    Admin view for notifications of accounts
    '''

    list_display = (
        'user',
        'is_read',
        'content',
        # 'message',
        'created',
    )
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        'is_read',
        'content',
        'created',
    )
    readonly_fields = (
        # 'message',
        'display_user_with_admin_url',
        'is_read',
        'content',
        'created',
    )
    search_fields = ('user', )
    date_hierarchy = 'created'
    fields = (
        'display_user_with_admin_url',
        'is_read',
        'content',
        # 'message',
        'created',
    )

    def display_user_with_admin_url(self, obj):
        return format_html('<a href="{}">{}</a>', obj.user.get_admin_url(), obj.user)
    display_user_with_admin_url.short_description = Notification._meta.get_field('user').verbose_name
