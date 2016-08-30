
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import forms


class OpinionFormSet(forms.BaseGenericInlineFormSet):

    def clean(self):

        super(OpinionFormSet, self).clean()

        if self.is_valid():

            # get users
            users = [data['user'] for data in self.cleaned_data]

            repeated_users = [user for user in users if users.count(user) > 1]

            if repeated_users:
                for form in self.forms:
                    if form.cleaned_data['user'] in repeated_users:
                        form.add_error('user', _('A same user not allowed to have more that one opinion.'))
