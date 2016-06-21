
from django.utils.html import format_html_join
from django.template.defaultfilters import truncatechars
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.solutions.models import Solution
from apps.articles.models import Article
from mylabour.utils import has_connect_to_internet

from .models import WebLink
from .listfilters import StatusWebLinkListFilter


class WebLinkAdmin(admin.ModelAdmin):
    '''
    Admin View for WebLink
    '''

    list_display = (
        'title',
        'show_short_url',
        'get_status',
    )
    search_fields = ('title', 'url')
    fieldsets = [
        [
            WebLink._meta.verbose_name, {
                'fields': ['title', 'url', 'where_used_as_html']
            }
        ]
    ]
    readonly_fields = ['where_used_as_html']

    def get_queryset(self, request):
        qs = super(WebLinkAdmin, self).get_queryset(request)
        qs = qs.weblinks_with_status()
        return qs

    def changelist_view(self, request, extra_context=None):
        #
        extra_context = extra_context or dict()
        #
        statistics = WebLink.objects.get_statistics_usage_web_links()
        extra_context['statistics'] = statistics
        #
        xdata = [
            Solution._meta.verbose_name_plural.capitalize(),
            Article._meta.verbose_name_plural.capitalize(),
        ]
        ydata = [
            statistics['count_usage_in_solutions'],
            statistics['count_usage_in_articles'],
        ]
        data_for_chart = {
            'data_chart_usage_weblinks': {'x': xdata, 'y': ydata},
            'type_chart_usage_weblinks': 'pieChart',
            'container_chart_usage_weblinks': 'container_chart_usage_weblinks',
            'extra_config': {
                'x_is_date': False,
                'x_axis_format': '',
                'tag_script_js': True,
                'jquery_on_ready': True,
            }
        }
        #
        extra_context.update(data_for_chart)
        response = super(WebLinkAdmin, self).changelist_view(request, extra_context)
        return response

    def get_list_filter(self, request):
        listfilters = super(WebLinkAdmin, self).get_list_filter(request)
        if has_connect_to_internet():
            listfilters = list(listfilters)
            listfilters.append(StatusWebLinkListFilter)
        return listfilters

    def show_short_url(self, obj):
        return truncatechars(obj.url, 100)
    show_short_url.short_description = WebLink._meta.get_field('url').verbose_name
    show_short_url.admin_order_field = 'url'

    def where_used_as_html(self, obj):
        pattern = '<li style="list-style:none;"><b>{0}</b>: <a href="{1}">"{2}"</a></li>'
        return format_html_join(
            '\n',
            pattern,
            ((obj._meta.verbose_name, obj.get_admin_page_url(), obj.title) for obj in obj.where_used())
        )
    where_used_as_html.short_description = _('Where used')
