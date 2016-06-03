
import collections

from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import forms


class ReplyFormSet(forms.BaseGenericInlineFormSet):

    def clean(self):
        super(ReplyFormSet, self).clean()
        all_given_reply_users = (form.cleaned_data.get('account') for form in self.forms)
        counter_all_given_reply_users = collections.Counter(all_given_reply_users)
        for form in self.forms:
            account = form.cleaned_data.get('account')
            if account and counter_all_given_reply_users[account] > 1:
                form.add_error('account', _('Please, don`t repeat user.'))
