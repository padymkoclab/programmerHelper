
import logging

from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin


class AdminSite:

    admin_site_title = _('')
    _empty_value_display = '-'

    show_calendar = True
    type_calendar = 'Form or Other Media object'
    # (Viewing calendar, adding events, dragging events)
    Full_Calendar = True

    WYSIWYG_Editors = ('TinyMCE', 'CREditor', 'Aloha Editor')

    Media_Gallery = True

    @property
    def empty_value_display(self):
        return self._empty_value_display

    def has_permission(self, request):
        """
        Returns True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        """
        return request.user.is_active and request.user.is_staff

    def each_context(self, request):

        return {
            '': '',
        }

    def get_urls(self):
        return []

    def wrap_as_admin_view(self):
        pass

    @property
    def urls(self):
        return self.get_urls()

    def password_change(self, request):
        pass

    def password_change_done(self, request):
        pass

    def login(self, request):
        pass

    def logout(self, request):
        pass

    def settings_view(self, request):
        pass

    def constants_view(self, request):
        pass


class AppAdmin:

    def app_index(self, request):
        pass

    def statistics_view(self, request, obj=None):
        pass

    def reports_view(self, request, obj=None):
        pass


class ModelAdmin:

    def add_view(self, request):
        pass

    def change_view(self, request, obj=None):
        pass

    def preview_view(self, request, obj=None):
        pass

    def delete_view(self, request):
        pass


class OtherAdmin:

    pass
