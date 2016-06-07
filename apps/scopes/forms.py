
from collections import Counter

from django.contrib.contenttypes.forms import BaseGenericInlineFormSet
from django.utils.translation import ugettext_lazy as _
from django import forms


class ScopeFormSet(BaseGenericInlineFormSet):
    """
    Special inline form for relationship between TestQuestion and Varian models.
    """

    def clean(self):
        """Custom validation"""

        super(ScopeFormSet, self).clean()
        all_given_scope_users = (form.cleaned_data.get('account') for form in self.forms)
        counter_all_given_scope_users = Counter(all_given_scope_users)
        for form in self.forms:
            account = form.cleaned_data.get('account')
            if account and counter_all_given_scope_users[account] > 1:
                form.add_error('account', _('Please, don`t repeat user.'))