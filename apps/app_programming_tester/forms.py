
from collections import Counter

from django.utils.translation import ugettext_lazy as _
from django.forms import BaseInlineFormSet, ValidationError


class VariantInlineFormSet(BaseInlineFormSet):
    """
    Special inline form for relationship between TestQuestion and Varian models.
    """

    def clean(self):
        """
        Validation what one variant is true.
        """

        super(VariantInlineFormSet, self).clean()
        lst = list()
        for form in self.forms:
            v = form.cleaned_data.get('is_right_variant', None)
            lst.append(v)
        count_right_variants = Counter(lst)[True]
        if count_right_variants != 1:
            if count_right_variants > 1:
                raise ValidationError(
                    _('Answer must be have only one right variant of answer.'),
                    code='required',
                )
            raise ValidationError(
                _('Answer must be have single right variant of answer.'),
                code='required',
            )
