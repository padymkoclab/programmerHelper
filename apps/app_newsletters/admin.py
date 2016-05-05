
# from django.utils.translation import ugettext_lazy as _
from django.contrib import admin


class NewsletterAdmin(admin.ModelAdmin):
    '''
        Admin View for News
    '''
    list_display = ('title', 'author', 'web_link', 'is_new', 'date_modified', 'date_added')
    list_filter = (
        ('author', admin.RelatedFieldListFilter),
        'date_modified',
        'date_added',
    )
    search_fields = ('title', 'web_link')
    date_hierarchy = 'date_added'
    fields = ['title', 'content', 'author', 'web_link']
