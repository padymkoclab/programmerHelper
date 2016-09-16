
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import forms

from utils.django.formsets_utils import find_dublication_on_formset

from .models import Reply


class ReplyAdminFormSet(forms.BaseGenericInlineFormSet):

    def clean(self):
        super().clean()

        find_dublication_on_formset(
            self,
            'user',
            _('On the form presents dublicate user'),
            Reply.ERROR_MSG_UNIQUE_USER_AND_OBJECT,
        )
