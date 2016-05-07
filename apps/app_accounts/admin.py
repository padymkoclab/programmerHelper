
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from mylabour.admin_listfilters import ListFilterLastLogin
from mylabour.admin_actions import (
    make_accounts_as_non_superuser,
    make_accounts_as_superuser,
    make_accounts_as_non_active,
    make_accounts_as_active,
    )

from .forms import UserChangeForm, UserCreationForm


class AccountAdmin(BaseUserAdmin):
    """
    Admin configuration for model Account
    """

    form = UserChangeForm
    add_form = UserCreationForm
    actions = [make_accounts_as_non_superuser, make_accounts_as_superuser, make_accounts_as_non_active, make_accounts_as_active]

    list_display = ['email', 'username', 'account_type', 'is_active', 'is_superuser', 'last_login', 'date_joined']
    search_fields = ['email', 'username']
    list_filter = ['account_type', 'is_superuser', ListFilterLastLogin, 'date_joined']
    date_hierarchy = 'date_joined'
    ordering = ['date_joined']
    #
    radio_fields = {'gender': admin.VERTICAL}
    filter_horizontal = ['groups']
    filter_vertical = ['user_permissions']
    readonly_fields = ['last_login']
    fieldsets = [
        (
            _('Account information'), {
                'classes': ['wide'],
                'fields':
                    [
                        'email',
                        'username',
                        'password',
                        'picture',
                    ]
            },
        ),
        (
            _('Personal information'), {
                'fields':
                    [
                        'gender',
                        'real_name',
                        'date_birthday',
                    ]
            }
        ),
        (
            _('Presents in web'), {
                'fields':
                    [
                        'presents_on_gmail',
                        'presents_on_github',
                        'presents_on_stackoverflow',
                        'personal_website',
                    ]
            }
        ),
        (
            _('Permissions'), {
                'fields': [
                    'is_active',
                    'is_superuser',
                    'user_permissions',
                    'groups',
                ]
            }
        ),
    ]
    add_fieldsets = [
        (
            None, {
                'fields': [
                    'email',
                    'username',
                    'password1',
                    'password2',
                    'date_birthday',
                ]
            }
        )
    ]
