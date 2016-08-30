
import random
import datetime
import time

from django.template.response import TemplateResponse
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from apps.comments.admin import CommentGenericInline
from apps.opinions.admin import OpinionGenericInline
from apps.opinions.admin_mixins import ScopeMixin
from apps.favours.admin import FavourInline

from .models import Snippet
from .forms import SnippetForm


class SnippetAdmin(ScopeMixin, admin.ModelAdmin):
    '''
    Admin View for Snippet.
    '''

    form = SnippetForm
    list_display = (
        'title',
        'account',
        'lexer',
        # 'views',
        'colored_scope',
        'get_count_comments',
        'get_count_tags',
        'get_count_opinions',
        'get_count_favours',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        ('account', admin.RelatedOnlyFieldListFilter),
        ('lexer', admin.AllValuesFieldListFilter),
        'date_modified',
        'date_added',
    )
    inlines = [
        OpinionGenericInline,
        FavourInline,
        CommentGenericInline,
    ]
    search_fields = ('title', 'account__username')
    filter_horizontal = ['tags']
    date_hierarchy = 'date_added'
    fieldsets = [
        [
            Snippet._meta.verbose_name, {
                'fields': ['title', 'account', 'lexer', 'description', 'code', 'tags']
            }
        ]
    ]

    def get_queryset(self, request):
        qs = super(SnippetAdmin, self).get_queryset(request)
        qs = qs.snippets_with_total_counters_on_related_fields()
        return qs

    def get_urls(self):
        urls = super(SnippetAdmin, self).get_urls()

        # a url name must be as 'snippets_snippet_statistics'
        url_name = 'statistics'
        name_for_url = '{0}_{1}_{2}'.format(self.model._meta.app_label, self.model._meta.model_name, url_name)

        # adding new url
        additional_urls = [
            url(r'^{0}/$'.format(url_name), self.admin_site.admin_view(self.statistics_view), {}, name_for_url),
        ]
        return additional_urls + urls

    def statistics_view(self, request):
        """ """

        # get data for charts
        # statistics_by_usage_lexers = Snippet.objects.get_statistics_by_usage_all_lexers()
        # only_used_lexers = tuple(couple[0] for couple in statistics_by_usage_lexers if couple[1] > 0)
        # only_values_of_used_lexers = tuple(couple[1] for couple in statistics_by_usage_lexers if couple[1] > 0)
        # # make charts
        # xdata = only_used_lexers
        # ydata = only_values_of_used_lexers
        # extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
        # usage_lexers_chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
        # usage_lexers_charttype = "pieChart"
        # piechart_usage_lexers_container = 'piechart_usage_lexers_container'
        # data = {
        #     'usage_lexers_charttype': usage_lexers_charttype,
        #     'usage_lexers_chartdata': usage_lexers_chartdata,
        #     'piechart_usage_lexers_container': piechart_usage_lexers_container,
        # }
        # adding variables to context
        context = dict(
            # Include common variables for rendering the admin template
            self.admin_site.each_context(request),
            title=_('Statistics by tags'),
            opts=self.model._meta,
            # root_path=self.admin_site.root_path,
        )
        # context.update(data)
        # context['statistics_by_usage_all_lexers'] = Snippet.objects.get_statistics_by_usage_all_lexers()
        # context['statistics_by_usage_tags'] = Snippet.tags_manager.get_statistics_by_count_used_tags()

        #
        #
        #

        xdata = [datetime.date(11, 11, 11), datetime.date(11, 11, 12), datetime.date(11, 11, 13), datetime.date(11, 11, 14)]
        ydata = [4, 2, 2, 1]
        tooltip_date = "%d %b %Y %H:%M:%S %p"
        extra_serie1 = {"tooltip": {"y_start": "", "y_end": " calls"}, "date_format": tooltip_date}
        chartdata = {
            'x': xdata,
            'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie1,
        }
        charttype = "cumulativeLineChart"
        data = {
            'charttype': charttype,
            'chartdata': chartdata,
        }
        context.update(data)

        return TemplateResponse(request, 'admin/snippets/statistics.html', context)

    def preview_snippet(self):
        """ """

        raise NotImplementedError

    def get_count_comments(self, obj):
        return obj.count_comments
    get_count_comments.admin_order_field = 'count_comments'
    get_count_comments.short_description = _('Count comments')

    def get_count_opinions(self, obj):
        return obj.count_opinions
    get_count_opinions.admin_order_field = 'count_opinions'
    get_count_opinions.short_description = _('Count opinions')

    def get_count_tags(self, obj):
        return obj.count_tags
    get_count_tags.admin_order_field = 'count_tags'
    get_count_tags.short_description = _('Count tags')

    def get_count_favours(self, obj):
        return obj.count_favours
    get_count_favours.admin_order_field = 'count_favours'
    get_count_favours.short_description = _('Count favours')
