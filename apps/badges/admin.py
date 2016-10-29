
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

from apps.admin.admin import ModelAdmin, TabularInline
from apps.admin.app import AppAdmin
from apps.admin.utils import register_app, register_model

from .models import Badge, EarnedBadge
from .apps import BadgesConfig


@register_app
class BadgesAppAdmin(AppAdmin):

    app_config_class = BadgesConfig


class UserInline(TabularInline):
    """
    Inline for users got a badge
    """

    model = Badge.users.through
    readonly_fields = ('user', )
    verbose_name_plural = _('Users')
    extra = 0
    max_num = 200


@register_model(Badge)
class BadgeAdmin(ModelAdmin):
    """
    Admin View for Badge
    """

    list_display = (
        'name',
        'category',
        'kind',
        'description',
        'get_count_awarded_users',
        'get_date_latest_awarded',
        'get_lastest_awarded_user',
    )
    list_filter = []
    search_fields = ('name', 'description')
    fieldsets = (
        (
            Badge._meta.verbose_name, {
                'fields': ['name', 'description'],
            }
        ),
    )
    inlines = [
        UserInline,
    ]

    def get_queryset(self, request):
        qs = super(BadgeAdmin, self).get_queryset(request)
        qs = qs.annotate(count_user_with_this_badge=Count('users'))
        return qs


@register_model(EarnedBadge)
class EarnedBadgeAdmin(ModelAdmin):
    '''
    Admin View for GettingBadge
    '''

    list_display = ('badge', 'user', 'created')
    # list_filter = (
    #     ('user', admin.RelatedOnlyFieldListFilter),
    #     ('badge', admin.RelatedOnlyFieldListFilter),
    #     'created',
    # )
    date_hierarchy = 'created'
    readonly_fields = ('badge', 'user', 'created')
    fieldsets = [
        [
            EarnedBadge._meta.verbose_name, {
                'fields': ('badge', 'user', 'created'),
            }
        ]
    ]
