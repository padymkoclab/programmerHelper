
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from apps.core.admin import AppAdmin, AdminSite

from .models import Newsletter
from .forms import NewsletterAdminModelForm
from .apps import NewslettersConfig


@AdminSite.register_app_admin_class
class NewsletterAppAdmin(AppAdmin):

    label = NewslettersConfig.label

    def get_context_for_tables_of_statistics(self):

        return (
            (
                _('Newsletters'), (
                    (_('Count newsletters'), Newsletter.objects.count()),
                ),
            ),
        )

    def get_context_for_charts_of_statistics(self):

        return (
            {
                'title': _('Chart count newsletters for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count newsletters')),
                    'data': Newsletter.objects.get_statistics_count_newsletters_for_the_past_year(),
                },
                'chart': Newsletter.objects.get_chart_count_newsletters_for_the_past_year(),
            },
        )


@admin.register(Newsletter, site=AdminSite)
class NewsletterAdmin(admin.ModelAdmin):
    '''
    Admin View for News
    '''

    form = NewsletterAdminModelForm
    list_display = ('truncated_content', 'date_added')
    list_filter = (
        'date_added',
    )
    search_fields = ('content', )
    date_hierarchy = 'date_added'
    readonly_fields = ('date_added', )

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            (
                Newsletter._meta.get_field('content').verbose_name, {
                    'classes': ('full-width', ),
                    'fields': ('content', ),
                }
            ),
        ]

        if obj is not None:

            fieldsets.append((
                _('Additional information'), {
                    'classes': ('collapse', ),
                    'fields': ('date_added', ),
                }
            ))

        return fieldsets

    def suit_cell_attributes(self, obj, column):

        if column == 'date_added':
            css_align = 'right'
        else:
            css_align = 'left'

        return {'class': 'text-{}'.format(css_align)}
