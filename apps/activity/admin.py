
from django.contrib import admin

from .models import Activity


class ActivityAdmin(admin.ModelAdmin):
    '''
    Admin view for activity
    '''

    list_display = ('account', 'message', 'flag', 'date')
    list_filter = (
        ('account', admin.RelatedOnlyFieldListFilter),
        'flag',
        'date',
    )
    readonly_fields = ('account', 'message', 'flag', 'date')
    search_fields = ('message',)
    date_hierarchy = 'date'
    fieldsets = [
        [
            Activity._meta.verbose_name, {
                'fields': ['account', 'flag', 'message'],
                'classes': ['wide'],
            }
        ]
    ]
