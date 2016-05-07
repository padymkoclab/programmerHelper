
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
    extra = 1


class VoteInPollInline(admin.TabularInline):
    '''
    Tabular Inline View for VoteInPoll
    '''

    model = VoteInPoll
    extra = 1


class PollAdmin(admin.ModelAdmin):
    '''
    Admin View for Poll
    '''

    list_display = ('title', 'get_count_votes', 'get_count_choices', 'accessability', 'status', 'status_changed')
    list_filter = ('accessability', 'status', 'date_modified', 'date_added')
    inlines = [
        ChoiceInline,
        VoteInPollInline,
    ]
    search_fields = ('title',)

    def get_queryset(self, request):
        qs = super(PollAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_votes=Count('votes', distinct=True),
            count_choices=Count('choices', distinct=True),
        )
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
    list_display = ('poll', 'text_choice')
    list_filter = (
        ('poll', admin.RelatedFieldListFilter),
    )
    search_fields = ('text_choice',)

admin.site.register(Choice, ChoiceAdmin)


class VoteInPollAdmin(admin.ModelAdmin):
    '''
        Admin View for VoteInPoll
    '''
    list_display = ('poll', 'user', 'choice', 'date_voting')
    list_filter = (
        ('poll', admin.RelatedFieldListFilter),
        ('user', admin.RelatedFieldListFilter),
        'choice',
        'date_voting',
    )
