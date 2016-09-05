
from django.utils.translation import ugettext_lazy as _

from django.forms import BaseInlineFormSet


class VariantInlineFormSet(BaseInlineFormSet):
    """
    Special inline form for relationship between TestQuestion and Varian models.
    """

    def clean(self):
        """
        Validation what one variant is true.
        """

        super(VariantInlineFormSet, self).clean()

    def get_unique_error_message(self, unique_check):

        if len(unique_check) == 1:
            return _("Please correct the duplicate data for %(field)s.") % {
                "field": unique_check[0],
            }
        else:
            return _("This question already has variant with that text.")
