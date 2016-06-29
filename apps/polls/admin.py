
from django.template.defaultfilters import truncatewords
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from .models import *


class ChoiceInline(admin.StackedInline):
    '''
    Stacked Inline View for Choice
    '''

    model = Choice
    min_num = Poll.MIN_COUNT_CHOICES_IN_POLL
    max_num = Poll.MAX_COUNT_CHOICES_IN_POLL
    extra = 0


class VoteInPollInline(admin.TabularInline):
    '''
    Tabular Inline View for VoteInPoll
    '''

    model = VoteInPoll
    extra = 0
    fields = ['choice', 'account']


class PollAdmin(admin.ModelAdmin):
    '''
    Admin View for Poll
    '''

    list_display = ('title', 'get_count_votes', 'get_count_choices', 'status', 'status_changed')
    list_filter = ('status', 'date_modified', 'date_added')
    list_select_related = ('choices', )
    inlines = [
        ChoiceInline,
        VoteInPollInline,
    ]
    search_fields = ('title',)
    fieldsets = [
        [
            Poll._meta.verbose_name, {
                'fields': ['title', 'status', 'status_changed']
            }
        ]
    ]

    def get_queryset(self, request):
        qs = super(PollAdmin, self).get_queryset(request)
        qs = qs.polls_with_count_choices_and_votes()
        return qs

    def get_count_votes(self, obj):
        return obj.count_votes
    get_count_votes.admin_order_field = 'count_votes'
    get_count_votes.short_description = _('Count votes')

    def get_count_choices(self, obj):
        return obj.count_choices
    get_count_choices.admin_order_field = 'count_choices'
    get_count_choices.short_description = _('Count choices')


class ChoiceAdmin(admin.ModelAdmin):
    '''
    Admin View for Choice
    '''

    list_display = ('__str__', 'poll', 'get_count_votes')
    list_filter = (
        ('poll', admin.RelatedOnlyFieldListFilter),
    )
    search_fields = ('text_choice',)
    fieldsets = [
        [
            Choice._meta.verbose_name, {
                'fields': ['poll', 'text_choice']
            }
        ]
    ]

    def get_queryset(self, request):
        qs = super(ChoiceAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_votes=Count('votes')
        )
        return qs

    def get_count_votes(self, obj):
        return obj.count_votes
    get_count_votes.short_description = _('Count votes')
    get_count_votes.admin_order_field = 'count_votes'

    def shorted_text_choice(self, obj):
        """Display long text choice as truncated."""

        return truncatewords(obj, 5)


class VoteInPollAdmin(admin.ModelAdmin):
    '''
        Admin View for VoteInPoll
    '''

    list_display = ('poll', 'account', 'choice', 'date_voting')
    list_filter = (
        ('poll', admin.RelatedOnlyFieldListFilter),
        ('account', admin.RelatedOnlyFieldListFilter),
        'choice',
        'date_voting',
    )
    readonly_fields = ['poll', 'account', 'choice']
    fieldsets = [
        [
            VoteInPoll._meta.verbose_name, {
                'fields': ['poll', 'account', 'choice']
            }
        ]
    ]
