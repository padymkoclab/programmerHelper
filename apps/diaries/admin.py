
import logging

from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from apps.core.admin import AdminSite

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
    form = PartitionInlineAdminModelForm
    fieldsets = (
        (
            None, {
                'fields': (
                    'name',
                    'content',
                )
            }
        ),
    )


@admin.register(Diary, site=AdminSite)
class DiaryAdmin(admin.ModelAdmin):

    fieldsets = [
        (
            None, {
                'fields': (
                    # 'user',
                )
            }
        )
    ]
    list_display = ('user', 'get_count_partitions', 'get_date_latest_changes')
    inlines = (PartitionInline, )

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        qs = qs.diaries_with_count_partitions()
        return qs
