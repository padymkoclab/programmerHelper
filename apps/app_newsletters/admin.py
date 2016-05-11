
from django.contrib import admin

from .models import Newsletter


class NewsletterAdmin(admin.ModelAdmin):
    '''
        Admin View for News
    '''
    list_display = ('title', 'author', 'web_link', 'is_new', 'date_modified', 'date_added')
    list_filter = (
        ('author', admin.RelatedOnlyFieldListFilter),
        'date_modified',
        'date_added',
    )
    search_fields = ('title', 'web_link')
    date_hierarchy = 'date_added'
    fieldsets = [
        [
            Newsletter._meta.verbose_name, {
                'fields': ['title', 'content', 'author', 'web_link']
            }
        ]
    ]
