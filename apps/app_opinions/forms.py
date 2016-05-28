
import collections

from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import forms


class OpinionFormSet(forms.BaseGenericInlineFormSet):

    def clean(self):
        super(OpinionFormSet, self).clean()
        if not self.total_error_count():
            accounts = (i['account'] for i in self.cleaned_data)
            counter_accounts = collections.Counter(accounts)
            repeated_accounts = tuple(item[0] for item in counter_accounts.items() if item[1] > 1)
            if repeated_accounts:
                self.non_form_errors().append(_('On form present the repeated users.'))
                for form in self.forms:
                    if form.cleaned_data['account'] in repeated_accounts:
                        form.add_error('account', _('Repeated account'))
