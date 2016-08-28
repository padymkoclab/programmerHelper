
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin


class BookSizeSimpleListFilter(admin.SimpleListFilter):
    """ """

    title = _('Book size')
    parameter_name = 'size'

    def lookups(self, request, model_admin):

        queryset = model_admin.get_queryset(request).books_with_sizes()

        if queryset.filter(size='tiny').exists():
            yield ('tiny', _('Tiny books'))
        if queryset.filter(size='middle').exists():
            yield ('middle', _('Middle books'))
        if queryset.filter(size='big').exists():
            yield ('big', _('Big books'))
        if queryset.filter(size='great').exists():
            yield ('great', _('Great books'))

    def queryset(self, request, queryset):

        queryset = queryset.books_with_sizes()

        value = self.value()
        if value == 'tiny':
            return queryset.filter(size='tiny')
        elif value == 'middle':
            return queryset.filter(size='middle')
        elif value == 'big':
            return queryset.filter(size='big')
        elif value == 'great':
            return queryset.filter(size='great')


class StatusLifeWriterSimpleListFilter(admin.SimpleListFilter):
    """ """

    title = _('Status life')
    parameter_name = 'status_life'

    def lookups(self, request, model_admin):

        queryset = model_admin.get_queryset(request)

        if queryset.filter(death_year=None).exists():
            yield ('alive', _('Alive writers'))
        if queryset.exclude(death_year=None).exists():
            yield ('dead', _('Dead writers'))

    def queryset(self, request, queryset):

        value = self.value()
        if value == 'alive':
            return queryset.filter(death_year=None)
        elif value == 'alive':
            return queryset.exclude(death_year=None)


class WritersCentriesSimpleListFilter(admin.SimpleListFilter):
    """ """

    title = _('Writers of centries')
    parameter_name = 'writers_centries'

    def lookups(self, request, model_amdin):

        return (
            ('20th', '20th centry'),
            ('21st', '21st centry'),
        )

    def queryset(self, request, queryset):

        value = self.value()
        if value == '20th':
            return queryset.filter(birth_year__lte=2000)
        elif value == '21st':
            return queryset.filter(
                models.Q(birth_year__gte=2000) |
                models.Q(death_year__gte=2000) |
                models.Q(death_year=None)
            )
