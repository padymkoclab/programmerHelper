
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin


class SessionExpireListFiler(admin.SimpleListFilter):
    pass


class ExtendedSessionAdmin(admin.ModelAdmin):
    '''
        Admin View for ExtendedSession
    '''
    list_display = ('display_account_name_insted_of_pk', 'session_key', 'status_session', 'expire_date')
    list_filter = (
        'expire_date',
        ('account_pk', admin.AllValuesFieldListFilter),
    )
    readonly_fields = ('account_pk', 'session_key', 'expire_date')
    date_hierarchy = 'expire_date'

    def display_account_name_insted_of_pk(self, obj):
        account = get_user_model().objects.get(pk=obj.account_pk)
        return account.__str__()
    display_account_name_insted_of_pk.short_description = _('Account')
