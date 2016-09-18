
from django.contrib.contenttypes.forms import BaseGenericInlineFormSet
from django.utils.translation import ugettext_lazy as _

from utils.django.formsets_utils import find_dublication_on_formset


class MarkAdminFormSet(BaseGenericInlineFormSet):
    """
    Special inline form for relationship between TestQuestion and Varian models.
    """

    def clean(self):
        """Custom validation"""

        super().clean()

        find_dublication_on_formset(
            self, 'user',
            _('A distinct user may give only a single mark'),
            _('Repeated user'),
        )
