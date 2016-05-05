
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from .models import WebLink


class SolutionInline(admin.TabularInline):
    '''
    Stacked Inline View for Solution
    '''

    model = WebLink.solutions.through
    extra = 1
    verbose_name_plural = _('Solutions')


class ArticleInline(admin.TabularInline):
    '''
    Stacked Inline View for Article
    '''

    model = WebLink.articles.through
    extra = 1
    verbose_name_plural = _('Articles')


class WebLinkAdmin(admin.ModelAdmin):
    '''
    Admin View for WebLink
    '''

    list_display = (
        'title',
        'web_url',
        'get_count_solutions_presents',
        'get_count_articles_presents',
    )
    search_fields = ('title', 'web_url')
    inlines = [
        SolutionInline,
        ArticleInline,
    ]
    fields = ['title', 'web_url']

    def get_queryset(self, request):
        qs = super(WebLinkAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_solutions=Count('solutions', distinct=True),
            count_articles=Count('articles', distinct=True),
        )
        return qs

    def get_count_solutions_presents(self, obj):
        return obj.count_solutions
    get_count_solutions_presents.admin_order_field = 'count_solutions'
    get_count_solutions_presents.short_description = _('In how many solution presents')

    def get_count_articles_presents(self, obj):
        return obj.count_articles
    get_count_articles_presents.admin_order_field = 'count_articles'
    get_count_articles_presents.short_description = _('In how many articles presents')
