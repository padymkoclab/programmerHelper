
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class DecadeBornListFilter(admin.SimpleListFilter):
    """
    A ListFilter for filter a users by decade born of year, on based date birth of each user.
    """

    title = _('Decade born')

    def lookups(self):
        return (
            ('', _('Born in the summer')),
            ('', _('Born in the winter')),
            ('', _('Born in the autumn')),
            ('', _('Born in the spring')),
        )

    def queryset(self, request, queryset):
        if self.values() == '':
            return
