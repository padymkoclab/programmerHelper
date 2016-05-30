
from django.contrib import admin

from .models import Inbox


class InboxAdmin(admin.ModelAdmin):
    '''
    Admin view for inboxes of accounts
    '''

    list_display = ('account', 'message', 'date_received')
    list_filter = (
        ('account', admin.RelatedOnlyFieldListFilter),
        'date_received',
    )
    readonly_fields = ('account', 'message',)
    search_fields = ('message',)
    date_hierarchy = 'date_received'
    fieldsets = [
        [
            Inbox._meta.verbose_name, {
                'fields': ['account', 'message'],
                'classes': ['wide'],
            }
        ]
    ]
