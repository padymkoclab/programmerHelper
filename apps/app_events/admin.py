
from django.contrib import admin

from .models import Event


class EventAdmin(admin.ModelAdmin):
    '''
    Admin view for events
    '''

    list_display = ('account', 'message', 'flag', 'date_action')
    list_filter = (
        ('account', admin.RelatedOnlyFieldListFilter),
        'flag',
        'date_action',
    )
    readonly_fields = ('account', 'message', 'flag', 'date_action')
    search_fields = ('message',)
    date_hierarchy = 'date_action'
    fieldsets = [
        [
            Event._meta.verbose_name, {
                'fields': ['account', 'flag', 'message'],
                'classes': ['wide'],
            }
        ]
    ]
