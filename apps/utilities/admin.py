
from unittest import mock

from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.apps import apps
from django.utils.text import force_text
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from mylabour.logging_utils import create_logger_by_filename
from mylabour.listfilters import IsNewSimpleListFilter

from apps.opinions.admin import OpinionGenericInline
from apps.comments.admin import CommentGenericInline

from .models import UtilityCategory, Utility
from .forms import UtilityCategoryAdminModelForm, UtilityAdminModelForm


logger = create_logger_by_filename(__name__)


class UtilityInline(admin.StackedInline):
    """
    Stacked Inline View for Utility
    """

    form = UtilityAdminModelForm
    model = Utility
    extra = 0
    fk_name = 'category'
    readonly_fields = ['get_mark', 'get_count_comments', 'get_count_opinions', 'date_modified', 'date_added']
    fields = [
        'name',
        'description',
        'category',
        'web_link',
        'get_mark',
        'get_count_comments',
        'get_count_opinions',
        'date_modified',
        'date_added',
    ]


class UtilityCategoryAdmin(admin.ModelAdmin):
    '''
    Admin View for UtilityCategory
    '''

    form = UtilityCategoryAdminModelForm
    list_display = (
        'name',
        'get_count_utilities',
        'get_total_mark',
        'get_total_count_opinions',
        'get_total_count_comments',
        'is_new',
        'date_modified',
        'date_added')
    list_filter = (
        IsNewSimpleListFilter,
        'date_modified',
        'date_added',
    )
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name', )}
    readonly_fields = [
        'get_total_mark',
        'get_total_count_opinions',
        'get_total_count_comments',
        'get_count_utilities',
        'date_modified',
        'date_added',
    ]

    def get_queryset(self, request):

        qs = super(UtilityCategoryAdmin, self).get_queryset(request)
        qs = qs.categories_with_all_additional_fields()
        return qs

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            [
                UtilityCategory._meta.verbose_name, {
                    'fields': [
                        'name',
                        'slug',
                        'description',
                        'image',
                    ]
                }
            ]
        ]

        if obj:
            fieldsets.append([
                _('Additional information'), {
                    'classes': ('collapse', ),
                    'fields': [
                        'get_total_mark',
                        'get_total_count_opinions',
                        'get_total_count_comments',
                        'get_count_utilities',
                        'date_modified',
                        'date_added',
                    ]
                }
            ])
        return fieldsets

    def get_inline_instances(self, request, obj=None):

        if obj:
            inlines = [UtilityInline]
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []


class UtilityAdmin(admin.ModelAdmin):
    '''
    Admin View for Utility
    '''

    form = UtilityAdminModelForm
    list_display = (
        'truncated_name',
        'category',
        'get_mark',
        'get_count_opinions',
        'get_count_comments',
        'is_new',
        'date_modified',
        'date_added',
    )

    logger.error('Does not working (\'category\', admin.RelatedOnlyFieldListFilter),')

    list_filter = (
        # ('category', admin.RelatedOnlyFieldListFilter),
        # https://code.djangoproject.com/ticket/26979
        IsNewSimpleListFilter,
        'date_modified',
        'date_added',
    )
    search_fields = ('name', )
    readonly_fields = ['get_mark', 'get_count_comments', 'get_count_opinions', 'date_modified', 'date_added']

    def get_queryset(self, request):
        qs = super(UtilityAdmin, self).get_queryset(request)
        qs = qs.utilities_with_all_additional_fields()
        return qs

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            [
                Utility._meta.verbose_name, {
                    'fields': [
                        'name',
                        'description',
                        'category',
                        'web_link',
                    ]
                }
            ],
        ]

        if obj:
            fieldsets.append([
                _('Additional information'), {
                    'classes': ('collapse', ),
                    'fields': [
                        'get_mark',
                        'get_count_comments',
                        'get_count_opinions',
                        'date_modified',
                        'date_added',
                    ]
                }
            ])

        return fieldsets

    def get_inline_instances(self, request, obj=None):

        if obj:
            inlines = [
                OpinionGenericInline,
                CommentGenericInline,
            ]
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def truncated_name(self, obj):
        return truncatechars(force_text(obj), 50)
    truncated_name.short_description = Utility._meta.get_field('name').verbose_name
    truncated_name.admin_order_field = 'name'


class AppAdmin:

    @property
    def admin_site(self):
        return admin.AdminSite()

    @property
    def media(self):
        return admin.ModelAdmin(mock.Mock(), self.admin_site).media

    def statistics_view(self, request, app_label):
        """ """

        # each custom app must be has template for statistics in own folder templates/app_label/admin/...
        template = '{0}/admin/statistics.html'.format(app_label)

        app_config = apps.get_app_config(app_label)

        app_name = app_config.verbose_name

        # context with statictis data
        app_statistics_context = {
            'count_categories': UtilityCategory.objects.count(),
            'avg_count_utilities_in_categories': UtilityCategory.objects.get_avg_count_utilities_in_categories(),
            'count_utilities': Utility.objects.count(),
            'avg_count_opinions_in_utilities': Utility.objects.get_avg_count_opinions_in_utilities(),
            'avg_count_comments_in_utilities': Utility.objects.get_avg_count_comments_in_utilities(),
            'count_opinions': Utility.objects.get_count_opinions(),
            'count_good_opinions': Utility.objects.get_count_good_opinions(),
            'count_bad_opinions': Utility.objects.get_count_bad_opinions(),
            'count_comments': Utility.objects.get_count_comments(),
            'count_users_posted_comments': Utility.objects.get_count_users_posted_comments(),
            'chart_most_popular_utilities': Utility.objects.get_chart_most_popular_utilities(),
            'most_popular_utilities': Utility.objects.get_most_popular_utilities(),
        }

        context = dict(
            self.admin_site.each_context(request),
            title=_('{0} statistics').format(app_name),
            app_name=app_name,
            app_label=app_label,
            statistics_data=app_statistics_context,
        )

        # for Django-Suit, especially for left Menu
        request.current_app = self.name

        return TemplateResponse(request, template, context)

    def reports_view(self, request, app_label):

        if request.method == 'GET':

            # each custom app must be has template for statistics in own folder templates/app_label/admin/...
            template = '{0}/admin/reports.html'.format(app_label)

            app_config = apps.get_app_config(app_label)

            app_name = app_config.verbose_name

            # context with statictis data
            app_themes_for_reports = {
                UtilityCategory._meta.verbose_name_plural: 'categories',
                Utility._meta.verbose_name_plural: 'utilities',
            }

            context = dict(
                self.admin_site.each_context(request),
                title=_('{0} reports').format(app_name),
                app_name=app_name,
                app_label=app_label,
                themes_for_reports=app_themes_for_reports,
                media=self.media,
            )

            # for Django-Suit, especially for left Menu
            request.current_app = self.name

            return TemplateResponse(request, template, context)

        elif request.method == 'POST':

            app_config = apps.get_app_config(app_label)

            output_report = request.POST['output_report']

            themes = request.POST.getlist('themes')

            themes = ', '.join(themes)

            msg = 'Report must generated in {0} on themes: {1}'.format(output_report.upper(), themes)

            return HttpResponse(msg)
