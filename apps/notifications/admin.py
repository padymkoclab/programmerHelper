
from django.utils.html import format_html
from django.contrib import admin

from apps.admin.admin import ModelAdmin
from apps.admin.app import AppAdmin
from apps.admin.site import DefaultSiteAdmin

from .models import Notification
from .apps import NotificationsConfig


class NotificationsAppAdmin(AppAdmin):

    app_config_class = NotificationsConfig


class NotificationModelAdmin(ModelAdmin):
    '''
    Admin view for notifications of accounts
    '''

    list_display = (
        'user',
        'is_read',
        'content',
        'action',
        'created',
    )
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        'is_read',
        'action',
        'created',
    )
    readonly_fields = (
        'action',
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
        'action',
        'created',
    )

    def display_user_with_admin_url(self, obj):
        return format_html('<a href="{}">{}</a>', obj.user.get_admin_url(), obj.user)
    # display_user_with_admin_url.short_description = Notification._meta.get_field('user').verbose_name


DefaultSiteAdmin.register_app(NotificationsAppAdmin)
DefaultSiteAdmin.register_model(Notification, NotificationModelAdmin)
