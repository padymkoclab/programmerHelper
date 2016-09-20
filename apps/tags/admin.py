
from django.utils.html import format_html
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from utils.django.models_utils import get_admin_url

from apps.core.admin import AdminSite, AppAdmin

from .models import Tag
from .apps import TagsConfig
from .forms import TagAdminModelForm
from .actions import delete_unused_tags


@AdminSite.register_app_admin_class
class ThisAppAdmin(AppAdmin):

    label = TagsConfig.label

    def get_context_for_tables_of_statistics(self):

        return (
            (_('Tags'), (
                (_('Count tags'), Tag.objects.count()),
            )),
        )

    def get_context_for_charts_of_statistics(self):

        return (
            {
                'title': _('Chart total usage tags by type objects'),
                'table': {
                    'fields': (_('Type object'), _('Count used tags')),
                    'data': Tag.objects.get_statistics_total_used_tags_by_type_objects()
                },
                'chart': Tag.objects.get_chart_total_used_tags_by_type_objects(),
            },
            {
                'title': _('Tags cloud'),
                'table': None,
                'chart': Tag.objects.display_cloud_tags(),
            },
        )


related_fields_names = Tag._get_related_fields_names()

inlines = list()
for related_field_name in related_fields_names:

    class_name = '{}InlineAdmin'.format(related_field_name.capitalize())

    ThroughModel = getattr(Tag, related_field_name).through
    OriginalModel = ThroughModel._meta.auto_created

    verbose_name = OriginalModel._meta.verbose_name
    verbose_name_plural = '{} (Here must be count!!!)'.format(OriginalModel._meta.verbose_name_plural)

    def truncated_object_with_change_link(self, obj):

        related_field_name = [field_name for field_name in obj._meta.unique_together[0] if field_name != 'tag'][0]

        related_field = getattr(obj, related_field_name)

        return format_html('<a href="{}">{}</a>', get_admin_url(related_field), truncatechars(related_field, 160))

    setattr(truncated_object_with_change_link, 'short_description', verbose_name)

    attrs = dict(
        model=ThroughModel,
        can_delete=False,
        max_num=0,
        verbose_name_plural=verbose_name_plural,
        show_change_link=True,
        classes=('collapse', ),
        fields=('truncated_object_with_change_link', ),
        readonly_fields=('truncated_object_with_change_link', ),
        suit_classes='suit-tab suit-tab-usage',
        truncated_object_with_change_link=truncated_object_with_change_link,
    )
    InlineModel = type(class_name, (admin.TabularInline, ), attrs)

    inlines.append(InlineModel)


@admin.register(Tag, site=AdminSite)
class TagAdmin(admin.ModelAdmin):
    '''
        Admin View for Tag
    '''

    actions = [delete_unused_tags]
    list_display = (
        'name',
        'truncated_description',
        'get_total_count_usage',
    )
    form = TagAdminModelForm

    # range count ListFilter
    search_fields = ('name', )
    readonly_fields = (
        'get_total_count_usage',
        'where_used',
    )

    suit_form_tabs = (
        ('general', _('General')),
        ('usage', _('Usage')),
        ('statistics', _('Statistics')),
    )

    def get_queryset(self, request):
        qs = super(TagAdmin, self).get_queryset(request)
        qs = qs.tags_with_total_count_usage()
        return qs

    def get_inline_instances(self, request, obj=None):

        if obj is not None:

            return [inline(self.model, self.admin_site) for inline in inlines]
        return ()

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            (
                Tag._meta.verbose_name, {
                    'classes': ('suit-tab', 'suit-tab-general'),
                    'fields': (
                        'name',
                        'description',
                    )
                }
            ),
        ]

        if obj is not None:

            fieldsets.append(
                (
                    _('Statistics'), {
                        'classes': ('suit-tab', 'suit-tab-statistics'),
                        'fields': (
                            'get_total_count_usage',
                        )
                    }
                ),
            )

        return fieldsets

    def suit_cell_attributes(self, request, column):

        if column == 'get_total_count_usage':
            css_align = 'center'
        else:
            css_align = 'left'

        return {'class': 'text-{}'.format(css_align)}

    def truncated_description(self, obj):

        return truncatechars(obj.description, 100)
    truncated_description.short_description = Tag._meta.get_field('description').verbose_name
    truncated_description.admin_order_field = 'description'
