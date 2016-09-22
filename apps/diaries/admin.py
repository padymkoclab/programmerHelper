
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
    fields = ('date_added', 'date_modified')
    readonly_fields = ('date_added', 'date_modified')
    verbose_name_plural = ''
    show_change_link = True

    suit_classes = 'suit-tab suit-tab-diary'

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
                # 'classes': ('collapse', ),
                'fields': (
                    'name',
                )
            }
        ),
        (
            None, {
                'classes': ('full-width', ),
                'fields': (
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
    inlines = (PartitionInline, )
