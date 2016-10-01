
from django.contrib.admin.checks import (
    BaseModelAdminChecks, InlineModelAdminChecks, ModelAdminChecks,
)
from django.conf.urls import url
from django.contrib.auth import get_permission_codename
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from django.utils.text import capfirst, get_text_list
from django.utils.translation import (
    override as translation_override, string_concat, ugettext as _, ungettext,
)
from django.views.decorators.csrf import csrf_protect
from django.views.generic import RedirectView

from .decorators import admin_staff_member_required
from .views import AddView, ChangeListView, ChangeView, HistoryView, DeleteView


class CheckModelAdmin:

    def check(self, admin_obj):

        errors = []

        # from django.views.generic import View

        # if not isinstance(admin_obj.changelist_view, View):
        #     raise ValueError('Model admin class must be passed changelist_view as CBV')
        #
        return errors


class ModelAdmin:

    # raw_id_fields = ()
    # fields = None
    # exclude = None
    # fieldsets = None
    # form = forms.ModelForm
    # filter_vertical = ()
    # filter_horizontal = ()
    # radio_fields = {}
    # prepopulated_fields = {}
    # formfield_overrides = {}
    # readonly_fields = ()
    # ordering = None
    # view_on_site = True
    # show_full_result_count = True

    list_display = ('__str__', )
    list_display_styles = (
        (
            '__all__', {
                'align': 'center',
            }
        ),
    )
    colored_rows_by = str()
    ordering = tuple()
    disabled_urls = tuple()
    # list_display_links = ()
    # list_filter = ()
    # list_select_related = False
    # list_per_page = 100
    # list_max_show_all = 200
    # list_editable = ()
    # search_fields = ()
    # date_hierarchy = None
    # save_as = False
    # save_as_continue = True
    # save_on_top = False
    # paginator = Paginator
    # preserve_filters = True
    # inlines = []

    # # Custom templates (designed to be over-ridden in subclasses)
    # add_form_template = None
    # change_form_template = None
    # change_list_template = None
    # delete_confirmation_template = None
    # delete_selected_confirmation_template = None
    # object_history_template = None

    # # Actions
    # actions = []
    # action_form = helpers.ActionForm
    # actions_on_top = True
    # actions_on_bottom = False
    # actions_selection_counter = True
    checks_class = CheckModelAdmin

    # views
    changelist_view = None

    def __init__(self, model, site_admin, **kwargs):
        self.model = model
        self.site_admin = site_admin

    def __str__(self):
        return 'ERRRO'.format()

    def check(self, **kwargs):
        return self.checks_class().check(self, **kwargs)

    def get_urls(self):

        app_label, model_name = self.model._meta.app_label, self.model._meta.model_name

        urls = dict(
            changelist=url(
                regex=r'^$', kwargs={}, name='{}_{}_changelist'.format(app_label, model_name),
                view=admin_staff_member_required(
                    ChangeListView.as_view(site_admin=self.site_admin, model_admin=self)
                ),
            ),
            add=url(
                regex=r'^add/$', kwargs={}, name='{}_{}_add'.format(app_label, model_name),
                view=admin_staff_member_required(
                    AddView.as_view(site_admin=self.site_admin, model_admin=self)
                ),
            ),
            change=url(
                regex=r'^(.+)/change/$', name='{}_{}_change'.format(app_label, model_name), kwargs={},
                view=admin_staff_member_required(
                    ChangeView.as_view(site_admin=self.site_admin, model_admin=self)
                ),
            ),
            history=url(
                regex=r'^(.+)/history/$', name='{}_{}_history'.format(app_label, model_name), kwargs={},
                view=admin_staff_member_required(
                    HistoryView.as_view(site_admin=self.site_admin, model_admin=self)
                ),
            ),
            delete=url(
                regex=r'^(.+)/delete/$', name='{}_{}_delete'.format(app_label, model_name), kwargs={},
                view=admin_staff_member_required(
                    DeleteView.as_view(site_admin=self.site_admin, model_admin=self)
                ),
            ),
        )

        urlpatterns = [url for url_name, url in urls.items() if url_name not in self.disabled_urls]

        # url(r'^(.+)/preview/$', wrap(self.change_view), name='%s_%s_preview' % info),
        # url(r'^(.+)/statistics/$', wrap(self.change_view), name='%s_%s_statistics' % info),
        # url(r'^(.+)/reports/$', wrap(self.change_view), name='%s_%s_reports' % info),

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()

    def get_queryset(self, request):

        qs = self.model._default_manager.get_queryset()

        ordering = self.get_ordering()

        if ordering:
            qs.order_by(*ordering)

        return qs

    def get_ordering(self):

        return self.ordering

    def get_list_display(self):

        return self.list_display

    def has_module_permissions(self, request):

        return request.user.has_module_permissions(self.model._meta.app_label)

    def get_model_permissions(self, request):

        return {
            'add': self.has_add_permission(request),
            'change': self.has_change_permission(request),
            'delete': self.has_delete_permission(request),
        }

    def has_add_permission(self, request):

        permission_codename = get_permission_codename('add', self.model._meta)
        permission = '{}.{}'.format(self.model._meta.app_label, permission_codename)
        return request.user.has_permission(permission)

    def has_change_permission(self, request):

        permission_codename = get_permission_codename('change', self.model._meta)
        permission = '{}.{}'.format(self.model._meta.app_label, permission_codename)
        return request.user.has_permission(permission)

    def has_delete_permission(self, request):

        permission_codename = get_permission_codename('delete', self.model._meta)
        permission = '{}.{}'.format(self.model._meta.app_label, permission_codename)
        return request.user.has_permission(permission)

    def get_list_display_styles(self):

        return self.list_display_styles

    def get_colored_rows_by(self):

        return self.colored_rows_by


class OtherAdmin:

    pass


class StackedInline:
    template = 'admin/edit_inline/stacked.html'


class TabularInline:
    template = 'admin/edit_inline/tabular.html'


class TableInline:
    template = 'admin/edit_inline/table.html'
