
from django.contrib import admin

from .models import Newsletter


class NewsletterAdmin(admin.ModelAdmin):
    '''
        Admin View for News
    '''
    list_display = ('title', 'account', 'web_link', 'is_new', 'date_modified', 'date_added')
    list_filter = (
        ('account', admin.RelatedOnlyFieldListFilter),
        'date_modified',
        'date_added',
    )
    search_fields = ('title', 'web_link')
    date_hierarchy = 'date_added'
    fieldsets = [
        [
            Newsletter._meta.verbose_name, {
                'fields': ['title', 'content', 'account', 'web_link']
            }
        ]
    ]
