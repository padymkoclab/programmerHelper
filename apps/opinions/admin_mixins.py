
import warnings
import statistics

from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html


class ScopeMixin(object):
    """Class-mixin for adding addionation methods to other ModelAdmins."""

    def colored_scope(self, obj):

        # determination ranges numbers
        # [min_scope, avg_min_scope, avg_scope, avg_max_scope, max_scope
        avg_scope = self.model.opinions_manager.get_avg_scope()
        max_scope = self.model.opinions_manager.get_max_scope()
        min_scope = self.model.opinions_manager.get_min_scope()
        avg_min_scope = statistics.mean([min_scope, avg_scope])
        avg_max_scope = statistics.mean([max_scope, avg_scope])

        # determination color and style displaying
        as_solid = True
        if min_scope <= obj.scope < avg_min_scope:
            color = 'red'
        elif avg_min_scope <= obj.scope <= avg_max_scope:
            color = 'black'
            as_solid = False
        elif avg_max_scope < obj.scope <= max_scope:
            color = 'green'
        else:
            warnings.warn('Scope out off range accepted values.')
            color = '000'

        # make html representation
        result = format_html(
            '<span style="color: {0};">{1}</span>',
            color,
            obj.scope
        )
        # adding solid displying if need
        if as_solid:
            result = format_html('<b>{0}</b>', result)

        return result
    colored_scope.short_description = _('Scope')
    colored_scope.admin_order_field = 'scope'
