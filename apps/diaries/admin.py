
import logging

from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from utils.django.datetime_utils import convert_date_to_django_date_format

# from apps.core.admin import AdminSite

from .models import Diary, Partition
from .forms import PartitionInlineAdminModelForm


class DiaryInline(admin.StackedInline):

    model = Diary
    template = 'users/admin/edit_inline/stacked_OneToOne.html'
    fields = ('created', 'updated')
    readonly_fields = ('created', 'updated')
    verbose_name_plural = ''
    show_change_link = True

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        # import ipdb; ipdb.set_trace()
        return qs

    # def get_fields(self, obj=None):

        # return (
        #     'user',
        # )


class PartitionInline(admin.StackedInline):

    extra = 1
    model = Partition
    readonly_fields = ('updated', )
    form = PartitionInlineAdminModelForm
    fieldsets = (
        (
            None, {
                'fields': (
                    'name',
                    'content',
                    'updated',
                )
            }
        ),
    )

    suit_classes = 'suit-tab suit-tab-partitions'


# @admin.register(Diary, site=AdminSite)
class DiaryAdmin(admin.ModelAdmin):

    readonly_fields = (
        'user',
        'get_count_partitions',
        'get_date_latest_changes_for_admin',
        'get_total_size',
    )
    fieldsets = [
        (
            None, {
                'classes': ('suit-tab', 'suit-tab-summary'),
                'fields': (
                    'user',
                    'get_count_partitions',
                    'get_date_latest_changes_for_admin',
                    'get_total_size',
                )
            }
        )
    ]
    list_display = (
        'user',
        'get_total_size',
        'get_count_partitions',
        'get_date_latest_changes',
    )
    inlines = (PartitionInline, )

    suit_form_tabs = (
        (('partitions'), _('Partitions')),
        (('summary'), _('Summary')),
    )

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        qs = qs.diaries_with_all_annotated_fields()
        return qs

    def suit_cell_attributes(self, request, column):

        if column in ['get_date_latest_changes']:
            css_class_align = 'right'
        elif column in ['user']:
            css_class_align = 'left'
        else:
            css_class_align = 'center'

        return {'class': 'text-{}'.format(css_class_align)}

    def get_date_latest_changes_for_admin(self, obj):
        """ """

        return convert_date_to_django_date_format(obj.date_latest_changes)
    get_date_latest_changes_for_admin.short_description = 'Date latest changes'
