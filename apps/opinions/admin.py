
from django.utils.translation import ugettext_lazy as _
from django.utils.text import force_text
from django.contrib.auth import get_user_model
from django.contrib.contenttypes import admin as admin_generic
from django.contrib import admin

from .models import Opinion
from .formsets import OpinionFormSet
from .forms import OpinionInlineAdminModelForm


User = get_user_model()


class OpinionGenericInline(admin_generic.GenericTabularInline):
    '''
    Stacked Inline View for Opinion
    '''

    form = OpinionInlineAdminModelForm
    formset = OpinionFormSet
    model = Opinion
    extra = 0
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
    fields = ['user', 'is_useful', 'updated', 'created']
    readonly_fields = ['updated', 'created']

    def get_max_num(self, request, obj=None, **kwargs):

        if obj:

            # count users without opinion about this object
            max_num = User._default_manager.count()

            # exclude an author of the object, if exists
            if hasattr(obj, 'user'):
                max_num -= 1

            return max_num
        return 0


class OpinionAdmin(admin.ModelAdmin):
    '''
    Admin View for Comment
    '''

    list_display = (
        'truncated_content_object',
        'content_type',
        'user',
        'is_useful',
        'updated',
        'created',
    )

    def truncated_content_object(self, obj):
        return force_text(obj.content_object)
    truncated_content_object.short_description = _('Object')
