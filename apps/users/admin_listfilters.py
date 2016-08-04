
from django.contrib import admin

from .models import UserLevel


class UserLevelRelatedOnlyFieldListFilter(admin.RelatedOnlyFieldListFilter):
    """ """

    def field_choices(self, field, request, model_admin):
        limit_choices_to = {'pk__in': set(model_admin.get_queryset(request).values_list(field.name, flat=True))}

        # replace name of level on pk
        pks = UserLevel.objects.filter(name__in=limit_choices_to['pk__in']).values_list('pk', flat=True)
        limit_choices_to = {'pk__in': set(pks)}

        return field.get_choices(include_blank=False, limit_choices_to=limit_choices_to)
