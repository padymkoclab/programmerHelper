
from django.contrib import admin

from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    '''
    Admin view for notifications of accounts
    '''

    list_display = ('account', 'message', 'date')
    list_filter = (
        ('account', admin.RelatedOnlyFieldListFilter),
        'date',
    )
    readonly_fields = ('account', 'message',)
    search_fields = ('message',)
    date_hierarchy = 'date'
    fieldsets = [
        [
            Notification._meta.verbose_name, {
                'fields': ['account', 'message'],
                'classes': ['wide'],
            }
        ]
    ]
