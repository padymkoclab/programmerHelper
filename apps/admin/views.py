
import operator
import functools
import logging
# import io
import json
# import collections

from django.contrib.admin import filters as django_filters
from django.core import serializers
from django.contrib.contenttypes.models import ContentType
# from django.http.request import QueryDict
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.response import TemplateResponse
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django import forms
# from django.utils.html import format_html, format_html_join
# from django.shortcuts import render, get_object_or_404
from django.db import models
# from django.apps import apps
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseBadRequest
# from django.db.models.fields.reverse_related import ManyToOneRel
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _, ungettext
from django.views import generic
from django.contrib.auth import login, logout
# from django.utils.text import capfirst
from django.utils.encoding import force_text

from utils.django.views_mixins import ContextTitleMixin
from utils.python.utils import get_filename_with_datetime

from .filters import DateTimeRangeFilter, RelatedOnlyFieldListFilter
from .forms_utils import BootstrapErrorList
from .forms import LoginForm, AddChangeDisplayForm, ImportForm, InlinesFormsets
from .utils import get_field_verbose_name_from_lookup
# from .descriptors import SiteAdminStrictDescriptor, ModelAdminStrictDescriptor
from .views_mixins import SiteAdminMixin, SiteModelAdminMixin, SiteAppAdminMixin


logger = logging.getLogger('django.development')


class SiteAdminView(generic.View):

    def get_context_data(self, **kwargs):

        context = dict()
        context.update(self.site_admin.each_context(self.request))
        context.update(**kwargs)

        return context


class IndexView(SiteAdminMixin, SiteAdminView):

    title = _('Index')

    def get(self, request, *args, **kwargs):

        return self.render_to_response(self.get_context_data())

    def render_to_response(self, context):

        return TemplateResponse(
            self.request,
            template=self.get_template_names(),
            context=context,
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_template_names(self):

        return (
            'admin/admin/index.html',
            )


class LoginView(ContextTitleMixin, generic.FormView):

    template_name = 'admin/admin/login.html'
    form_class = LoginForm
    title = _('Login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):

        login(self.request, form.get_user())

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('admin:index')


class LogoutView(generic.RedirectView):

    pattern_name = 'admin:login'
    permament = False

    def get_redirect_url(self, *args, **kwargs):

        logout(self.request)

        return super().get_redirect_url(*args, **kwargs)


class PasswordChangeView(generic.TemplateView):

    template_name = 'admin/admin/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(self.site_admin.each_context(self.request))

        context['title'] = _('Password change')

        return context


class PasswordChangeDoneView(generic.TemplateView):

    pass


class ChangeListView(SiteModelAdminMixin, SiteAdminView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_meta = self.model_admin.model._meta
        self.list_per_page = self.model_admin.list_per_page

        self.expected_parameters = set()
        self.filters = list()

    def post(self, request, *args, **kwargs):

        pks_selected_objects = request.POST.getlist('selected_objects')
        queryset = self.model_admin.model._default_manager.filter(pk__in=pks_selected_objects)

        if not queryset.exists():

            messages.add_message(
                request, messages.WARNING,
                "Items must be selected in order to perform actions on them. No items have been changed.",
                extra_tags='warning'
            )

            return self.render_to_response(request)

        action = request.POST.get('action')

        actions = self.model_admin.get_actions()

        # get function of action
        func = actions[action]['func']

        # make action
        func(self.model_admin, request, queryset)

        return self.render_to_response(request)

    def get(self, request, *args, **kwargs):

        self.set_filters()

        return self.render_to_response(request)

    def render_to_response(self, request):

        return TemplateResponse(
            request,
            template=self.get_template_names(),
            context=self.get_context_data()
            )

    def get_template_names(self):

        return [
            '{}/admin/{}/admin/changelist.html'.format(self.model_meta.app_label, self.model_meta.model_name),
            '{}/admin/admin/changelist.html'.format(self.model_meta.app_label),
            'admin/admin/changelist.html',
        ]

    @staticmethod
    def convert_search_field_to_lookup(search_field):

        if search_field.startswith('^'):
            return '{}__istartswith'.format(search_field.lstrip('^'))
        if search_field.endswith('$'):
            return '{}__iendswith'.format(search_field.rstrip('$'))
        if search_field.startswith('='):
            return '{}__iexact'.format(search_field.lstrip('='))
        else:
            return '{}__icontains'.format(search_field)

    def get_search_details(self):

        result = list()
        for search_field in self.model_admin.get_search_fields():

            if search_field.startswith('^'):
                field_name = search_field.lstrip('^')
                ignorecase = True
                type_search = 'Start swith'

            elif search_field.endswith('$'):
                field_name = search_field.rstrip('$')
                ignorecase = True
                type_search = 'End swith'

            elif search_field.startswith('='):
                field_name = search_field.lstrip('=')
                ignorecase = True
                type_search = 'Exact'

            else:
                field_name = search_field
                ignorecase = True
                type_search = 'Contains'

            field_name = get_field_verbose_name_from_lookup(field_name, self.model_admin.model)
            result.append({
                'ignorecase': ignorecase,
                'field_name': field_name,
                'type_search': type_search,
            })
        return result

    def filter_by_filter_restrictions(self, request, qs):

        for filter_ in self.filters:
            qs = filter_.queryset(request, qs)
        return qs

    def filter_by_search_restrictions(self, request, qs):

        search_fields = self.model_admin.get_search_fields()

        if search_fields:

            if self.q and search_fields:

                # make the same conditions for each field in the search_fields
                search_restrictions = {
                    self.convert_search_field_to_lookup(search_field): self.q
                    for search_field in search_fields
                }

                search_restrictions = functools.reduce(
                    operator.or_,
                    (models.Q(**{k: v}) for k, v in search_restrictions.items())
                )

                return qs.filter(search_restrictions)
            return qs

    def get_date_hierarchy_restrictions(self, request):

        if self.model_admin.date_hierarchy:

            restrictions = {}
            field_name = self.model_admin.date_hierarchy

            year_lookup = field_name + '__year'
            month_lookup = field_name + '__month'
            day_lookup = field_name + '__day'

            by_year = request.GET.get(year_lookup)
            by_month = request.GET.get(month_lookup)
            by_day = request.GET.get(day_lookup)

            if by_year is not None:
                restrictions[year_lookup] = by_year

            if by_month is not None:
                restrictions[month_lookup] = by_month

            if by_day is not None:
                restrictions[day_lookup] = by_day

            return restrictions

        return {}

    def get_queryset(self, request):

        # Queryset
        qs = self.model_admin.get_queryset(request)

        qs = self.filter_by_filter_restrictions(request, qs)
        qs = self.filter_by_search_restrictions(request, qs)

        # Ordering
        ordering = self.get_ordering()
        qs = qs.order_by(*ordering)

        # send message
        count = qs.count()
        object_name = self.model_meta.verbose_name if count == 1 else self.model_meta.verbose_name_plural
        object_name = object_name.lower()
        msg = ungettext(
            'Found {} {}',
            'Found {} {}',
            count
        ).format(count, object_name)
        self.model_admin.message_user(request, msg, extra_tags='info', level='INFO')

        return qs

    def get_ordering(self):

        ordering = self.model_admin.get_ordering()

        if not ordering:
            ordering = self.model_meta.ordering

        clickedColumn = self.request.GET.get('__clickedColumn')
        if clickedColumn is not None:
            ordering = self.determinate_dynamic_ordering(clickedColumn)

        return ordering or ()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        self.q = self.request.GET.get('q', '')
        self.q = self.q.strip()

        qs = self.get_queryset(self.request)

        list_per_page = self.request.GET.get('list_per_page', self.list_per_page)
        list_per_page = int(list_per_page)

        paginator = Paginator(qs, list_per_page)
        total_count_objects = paginator.count

        page = self.request.GET.get('page')

        try:
            page_object_list = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            page_object_list = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            page_object_list = paginator.page(page)

        list_per_page = total_count_objects if total_count_objects < list_per_page else list_per_page

        context.update({
            'title': _('Select {} to change').format(self.model_meta.verbose_name_plural.lower()),
            'model_meta': self.model_meta,
            'model_admin': self.model_admin,
            'q': self.q,
            'has_add_permission': self.model_admin.has_add_permission(self.request),
            'has_export_permission': self.model_admin.has_add_permission(self.request),
            'has_import_permission': self.model_admin.has_add_permission(self.request),
            'total_count_objects': total_count_objects,
            'list_per_page': list_per_page,
            'actions': self.model_admin.get_actions(),
            'page_object_list': page_object_list,
            'ordering': self.get_ordering(),
            'filters': self.filters,
            'search_details': self.get_search_details(),
        })

        return context

    def determinate_dynamic_ordering(self, clickedColumn):

        sortable_fields = self.request.GET.getlist('sortable_field')
        sortable_fields = [json.loads(i) for i in sortable_fields]

        concrete_fields = [i.name for i in self.model_meta.concrete_fields]

        ordering = list()
        for sortable_field in sortable_fields:
            for column_name, options in sortable_field.items():
                order = options['order']

                if order is not None or column_name == clickedColumn:

                    position = options['position']

                    if column_name == clickedColumn:
                        position = 1

                        order = options['order']
                        if options['order'] is None:
                            options['order'] = 'asc'
                        elif options['order'] == 'desc':
                            options['order'] = 'asc'
                        elif options['order'] == 'asc':
                            options['order'] = 'desc'
                    else:
                        position += 1

                    if column_name not in concrete_fields:
                        if hasattr(self.model_admin.model, column_name):
                            column_name = getattr(self.model_admin.model, column_name).admin_order_field
                        elif hasattr(self.model_admin, column_name):
                            column_name = getattr(self.model_admin, column_name).admin_order_field
                        else:
                            raise AttributeError('Instance has not method or field {}'.format(column_name))

                    if options['order'] == 'asc':
                        field_name = column_name
                    elif options['order'] == 'desc':
                        field_name = '-' + column_name

                    ordering.append((field_name, position))

            ordering.sort(key=lambda i: i[1])

        ordering = [i[0] for i in ordering]

        return ordering

    def set_filters(self):

        list_filter = self.model_admin.get_list_filter(self.request)

        for filter_ in list_filter:
            if isinstance(filter_, (tuple, list)):
                field_name, type_filter = filter_

                field = self.model_meta.get_field(field_name)

                if issubclass(type_filter, django_filters.RelatedOnlyFieldListFilter):
                    filter_ = RelatedOnlyFieldListFilter(field_name, field, self.model_meta.model)
            elif callable(filter_):
                if not issubclass(filter_, django_filters.SimpleListFilter):
                    raise TypeError(
                        'Own filter may be only an instance of the {}'.format(django_filters.SimpleListFilter)
                    )
            else:
                field_name, type_filter = filter_, None

                field = self.model_meta.get_field(field_name)

                if isinstance(field, (models.DateTimeField, models.DateField)):

                    filter_ = DateTimeRangeFilter(field_name, field, self.model_meta.model)

            self.filters.append(filter_)

            # ! resolve conficts parameters
            if hasattr(filter_, 'parameter_name'):
                self.expected_parameters.update(filter_.parameter_name)
            else:
                self.expected_parameters.update(filter_.expected_parameters)

    def get_querystring(self, **params):

        GET_ = self.request.GET.copy()

        for key, value in params.items():

            if value is None:
                GET_.pop(key, None)
            else:
                GET_[key] = value

        querystring = GET_.urlencode()

        return '?' + querystring


class AddView(SiteModelAdminMixin, SiteAdminView):

    def dispatch(self, request, *args, **kwargs):

        if not self.model_admin.has_change_permission(request):
            raise PermissionDenied

        return AddChangeView.as_view(model_admin=self.model_admin, site_admin=self.site_admin)(request)


class ChangeView(SiteModelAdminMixin, SiteAdminView):

    def dispatch(self, request, *args, **kwargs):

        if not self.model_admin.has_change_permission(request):
            raise PermissionDenied

        pk = kwargs['pk']

        # get_object_or_404 does not working with UUID
        try:
            obj = self.model_admin.model._default_manager.get(pk=pk)
        except (self.model_admin.model.DoesNotExist, ValueError):
            raise Http404(_('An object doesn`t found'))

        return AddChangeView.as_view(model_admin=self.model_admin, site_admin=self.site_admin)(request, obj)


class AddChangeView(SiteAdminView):

    model_admin = None
    site_admin = None

    def __init__(self, model_admin, site_admin, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_admin = model_admin
        self.site_admin = site_admin

        self.model_meta = self.model_admin.model._meta

    def dispatch(self, request, obj=None, *args, **kwargs):

        self.obj = obj

        return super().dispatch(request, *args, **kwargs)

    def get_title(self):

        if self.obj is not None:
            return _('Change {} "{}"').format(
                self.model_meta.verbose_name.lower(), self.obj
                )
        return _('Add {}').format(self.model_meta.verbose_name.lower())

    def get_context_data(self, **kwargs):

        context = super().get_context_data()

        context['title'] = self.get_title()
        context['object'] = self.obj
        context['has_add_permission'] = self.model_admin.has_add_permission(self.request)
        context['has_delete_permission'] = self.model_admin.has_delete_permission(self.request)
        context['model_admin'] = self.model_admin
        context['model_meta'] = self.model_meta

        if 'form' not in kwargs:
            modelform = self.get_modelform()
            form = self.get_form()
            form.media = modelform.media
            context['form'] = form
        else:
            context['form'] = kwargs.pop('form')

        inlines_formsets = kwargs.pop('inlines_formsets', self.get_inlines_formsets())

        context['inlines_formsets'] = InlinesFormsets(inlines_formsets, self.request)

        return context

    def get_template_names(self):

        return [
            '{}/admin/{}/addchange.html'.format(self.model_meta.app_label, self.model_meta.model_name),
            '{}/admin/addchange.html'.format(self.model_meta.app_label),
            'admin/admin/addchange.html',
        ]

    def render_to_response(self, context):

        return TemplateResponse(
            self.request,
            template=self.get_template_names(),
            context=self.get_context_data(),
        )

    def get(self, request, *args, **kwargs):

        return self.render_to_response(request)

    def post(self, request, *args, **kwargs):

        modelform = self.get_modelform()
        inlines_formsets = self.get_inlines_formsets()

        if modelform.is_valid():
            formsets = [formset for inline, formset in inlines_formsets]
            if forms.all_valid(formsets):
                return self.form_valid(modelform, formsets)
        return self.form_invalid(modelform, inlines_formsets)

    def get_form_class(self):

        return self.model_admin.get_form(self.request)

    def get_modelform(self):

        form = self.get_form_class()
        return form(instance=self.obj, **self.get_form_kwargs())

    def get_inlines_formsets(self):

        return self.model_admin.get_inlines_formsets(self.request, self.obj)

    def get_initial(self):

        if self.obj is None:
            return {}
        field_names = [i for i in self.get_form_class().base_fields]

        return {fieldname: getattr(self.obj, fieldname) for fieldname in field_names}

    def get_form_kwargs(self):

        kwargs = dict(initial=self.get_initial())

        if self.request.method == 'POST':

            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })

        return kwargs

    def get_form(self):

        return AddChangeDisplayForm(
            self.get_modelform(),
            fieldsets=self.model_admin.get_fieldsets(self.request, self.obj),
            readonly_fields=self.model_admin.get_readonly_fields(self.request, self.obj),
            model_admin=self.model_admin,
        )

    def form_invalid(self, form, inlines_formsets):

        object_name = self.model_meta.verbose_name.lower()

        if self.obj is None:
            msg = _('Could not create a new {}').format(object_name)
        else:
            msg = _('Could not update the {} "{}"').format(object_name, self.obj)

        self.model_admin.message_user(self.request, msg, 'ERROR', 'error')

        return self.render_to_response(
            context=self.get_context_data(
                form=form,
                inlines_formsets=inlines_formsets,
            )
        )

    def form_valid(self, form, formsets):

        self.object = form.save(commit=False)

        self.object.save()

        for formset in formsets:
            formset.save()

        object_name = self.model_meta.verbose_name.lower()

        if self.obj is None:
            extra_tags = 'created'
            msg = _('Succefully created new {} "{}"').format(object_name, self.object)
        else:
            extra_tags = 'updated'
            msg = _('Succefully updated {} "{}"').format(object_name, self.object)

        self.model_admin.message_user(self.request, msg, 'SUCCESS', extra_tags)

        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def get_success_url(self):

        _clicked_button = self.request.POST['_clicked_button']

        if _clicked_button == 'save':
            return self.site_admin.get_url('changelist', self.model_meta)
        elif _clicked_button == 'save_and_add_another':
            return self.site_admin.get_url('add', self.model_meta)
        elif _clicked_button == 'save_and_continue':
            return self.site_admin.get_url('change', self.model_meta, kwargs={'pk': self.object.pk})


class AppIndexView(SiteAppAdminMixin, SiteAdminView):

    def get(self, request, *args, **kwargs):

        return self.render_to_response(self.get_context_data())

    def get_template_names(self):

        return (
            'admin/admin/app_index.html',
        )

    def render_to_response(self, context):

        return TemplateResponse(
            self.request,
            template=self.get_template_names(),
            context=context,
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['title'] = self.app_config.verbose_name
        context['app_name'] = self.app_config.verbose_name
        context['app_models_info'] = self.get_app_models_info()
        context['reports_url'] = self.site_admin.get_url('reports', self.app_config.label)
        context['statistics_url'] = self.site_admin.get_url('statistics', self.app_config.label)

        return context

    def get_app_models_info(self):

        info = list()
        for model in self.app_config.get_models():

            if self.site_admin.is_registered_model(model):
                info.append((
                    force_text(model._meta.verbose_name),
                    self.site_admin.get_url('changelist', model._meta),
                    model._default_manager.count(),
                    ))

        info.sort(key=lambda x: x[0].lower())

        return info


class AppReportView(SiteAppAdminMixin, SiteAdminView):

    def dispatch(self, request, *args, **kwargs):
        self.app_admin = self.site_admin._registry_apps[self.app_config.label]

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):

        report_type = request.POST.get('report_type')
        report_code = request.POST.get('report_code')

        if report_type not in ['pdf', 'excel']:
            return HttpResponseBadRequest('Incorrect input data')

        return self.app_admin.get_report(request, report_type, report_code)

    def get_template_names(self):

        return (
            'admin/admin/reports.html',
        )

    def render_to_response(self, context):

        return TemplateResponse(
            self.request,
            template=self.get_template_names(),
            context=context,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = _('{} - Reports ').format(self.app_config.verbose_name)

        context['app_config'] = self.app_config
        context['reports_details'] = self.app_admin.reports

        return context


class AppStatisticsView(SiteAppAdminMixin, SiteAdminView):

    def get(self, request, *args, **kwargs):

        self.app_admin = self.site_admin._registry_apps[self.app_config.label]

        return self.render_to_response(self.get_context_data())

    def get_template_names(self):

        return (
            'admin/admin/statistics.html',
        )

    def render_to_response(self, context):

        return TemplateResponse(
            self.request,
            template=self.get_template_names(),
            context=context,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = _('{} - Statistics ').format(self.app_config.verbose_name)

        context['app_config'] = self.app_config
        context['tables_of_statistics'] = self.app_admin.get_tables_of_statistics()
        context['charts_of_statistics'] = self.app_admin.get_charts_of_statistics()

        return context


class HistoryView(SiteModelAdminMixin, generic.DetailView):

    pass


class DeleteView(SiteModelAdminMixin, generic.DeleteView):

    pk_url_kwarg = 'pk'
    context_object_name = 'object'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = self.model_admin.model
        self.model_meta = self.model._meta

    def dispatch(self, request, *args, **kwargs):

        if not self.model_admin.has_delete_permission(request):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):

        return [
            '{}/admin/{}/confirm_delete.html'.format(self.model_meta.app_label, self.model_meta.model_name),
            '{}/admin/confirm_delete.html'.format(self.model_meta.app_label),
            'admin/admin/confirm_delete.html',
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_meta'] = self.model_meta
        context['related_objects'] = self.get_related_objects()
        context['title'] = _('Delete {}').format(
            self.model_meta.verbose_name.lower()
            )

        return context

    def get_success_url(self):

        return self.site_admin.get_url('changelist', self.model_meta)

    def get_related_objects(self):

        related_objects = list()

        candidate_relations_to_delete = [
            i for i in self.object._meta.get_fields(include_hidden=True)
            if i.auto_created and not i.concrete and (i.one_to_one or i.one_to_many)
            ]

        for relationship in candidate_relations_to_delete:
            if relationship.on_delete != models.DO_NOTHING:

                related_model = relationship.related_model
                type_relationship = relationship.on_delete.__name__
                objects = related_model._base_manager.filter(
                    **{'{}__in'.format(
                        relationship.field.name): [self.object.pk]}
                    )

                related_objects.append(
                    (related_model._meta, type_relationship, objects)
                    )

        return related_objects

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()

        messages.add_message(
            request,
            messages.SUCCESS,
            _('Successfully deleted {} "{}"').format(self.model_meta.verbose_name.lower(), self.object),
            extra_tags='deleted',

            )

        return HttpResponseRedirect(success_url)


class ExportIndexView(SiteAdminMixin, generic.TemplateView):

    template_name = 'admin/admin/export.html'
    title = _('Export')


class ExportModelView(SiteAdminMixin, SiteAdminView):

    def get(self, request, *args, **kwargs):

        self.pk_model = kwargs['pk_model']
        self.listing_pks_objects = kwargs['listing_pks_objects']

        self.output_format = request.GET.get('output_format')

        # if is submit data
        if self.output_format is not None:

            if '__preview' in request.GET.keys():
                return self.preview()
            elif '__export' in request.GET.keys():
                return self.export()

        return self.render_to_response(request)

    def get_template_names(self):

        return [
            'admin/admin/export_model.html',
        ]

    def render_to_response(self, request):

        return TemplateResponse(
            request,
            template=self.get_template_names(),
            context=self.get_context_data(),
        )

    def get_model_content_type(self):

        pk_model = int(self.pk_model)
        model_content_type = ContentType.objects.get(pk=pk_model)

        return model_content_type

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        qs = self.get_queryset()

        context['title'] = _('Export {}').format(qs.model._meta.verbose_name_plural.lower())
        context['queryset'] = qs
        context['model_meta'] = qs.model._meta
        context['pk_model'] = self.pk_model

        return context

    def get_queryset(self):

        listing_pks_objects = self.listing_pks_objects.split(',')

        model_content_type = self.get_model_content_type()

        qs = model_content_type.get_all_objects_for_this_type(pk__in=listing_pks_objects)

        return qs

    def get_serialized_data(self):
        fields = self.request.GET.getlist('fields')

        pks_selected_objects_for_export = self.request.GET.getlist('pks_selected_objects_for_export')

        model_content_type = self.get_model_content_type()
        queryset = model_content_type.get_all_objects_for_this_type(pk__in=pks_selected_objects_for_export)

        return serializers.serialize(self.output_format, queryset, fields=fields)

    def get_response_with_serialised_data(self):
        content_type = 'text/' + self.output_format
        response = HttpResponse(content_type=content_type)
        data = self.get_serialized_data()
        response.write(data)
        return response

    def preview(self):

        return self.get_response_with_serialised_data()

    def export(self):

        response = self.get_response_with_serialised_data()

        model_content_type = self.get_model_content_type()
        model_meta = model_content_type.model_class()._meta

        filename = get_filename_with_datetime(model_meta.verbose_name_plural, self.output_format)
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

        return response


class ImportView(SiteAdminMixin, SiteAdminView):

    title = _('Import')

    def get(self, request, *args, **kwargs):

        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):

        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def render_to_response(self, context):

        return TemplateResponse(
            self.request,
            template=self.get_template_names(),
            context=context,
        )

    def get_context_data(self, **kwargs):

        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()

        return super().get_context_data(**kwargs)

    def get_template_names(self):

        return (
            'admin/admin/import.html',
        )

    def form_valid(self, form):

        file = form.files['file']
        content = file.read()

        if file.content_type == 'application/octet-stream':
            format_ = 'json'
        elif file.content_type == 'application/x-yaml':
            format_ = 'yaml'
        elif file.content_type == 'text/xml':
            content = content.decode('utf-8')
            format_ = 'xml'
        elif file.content_type == 'text/csv':
            format_ = 'csv'

        deserialize_objects = serializers.deserialize(format_, content)
        deserialize_objects = tuple(deserialize_objects)

        first_obj = deserialize_objects[0].object
        model_meta = first_obj._meta
        qs = model_meta.model._default_manager.all()
        pks = qs.values_list('pk', flat=True)

        count_inconsistent_objects = int()
        count_consistent_objects = int()
        objects = list()

        for deserialize_object in deserialize_objects:

            obj = deserialize_object.object

            logger.warning('Made function find_conflicts if it imported!')

            if obj.pk in pks:
                is_consistend = False
                count_inconsistent_objects += 1
            else:
                is_consistend = True
                count_consistent_objects += 1

            objects.append((obj.pk, obj, is_consistend))

        import_details = dict(
            objects=objects,
            model_meta=model_meta,
            count_objects_for_import=len(deserialize_objects),
            count_exists_objects=qs.count(),
            count_inconsistent_objects=count_inconsistent_objects,
            count_consistent_objects=count_consistent_objects,
        )

        return self.render_to_response(self.get_context_data(import_details=import_details))

    def form_invalid(self, form):

        return self.render_to_response(self.get_context_data(form=form))

    def get_form(self):

        return ImportForm(error_class=BootstrapErrorList, **self.get_form_kwargs())

    def get_form_kwargs(self):

        kwargs = {}

        if self.request.method == 'POST':
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })

        return kwargs


class SettingsView(SiteAdminMixin, SiteAdminView):

    template_name = ''

    # constants
