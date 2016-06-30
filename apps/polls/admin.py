

from django.utils.safestring import mark_safe
from django.template.defaultfilters import truncatechars
from django.utils.html import format_html_join, format_html
from django.template.defaultfilters import truncatewords
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
# from django.conf import settings

import pygal

from .models import Poll, Choice, VoteInPoll
from .forms import PollModelForm, ChoiceModelForm
from .formsets import ChoiceInlineFormSet


class ChoiceInline(admin.StackedInline):
    '''
    Stacked Inline View for Choice
    '''

    form = ChoiceModelForm
    formset = ChoiceInlineFormSet
    model = Choice
    min_num = Poll.MIN_COUNT_CHOICES_IN_POLL
    max_num = Poll.MAX_COUNT_CHOICES_IN_POLL
    extra = 0
    list_select_related = ('poll',)
    template = 'polls/admin/stacked.html'


class VoteInPollInline(admin.TabularInline):
    '''
    Tabular Inline View for VoteInPoll
    '''

    list_select_related = ('poll', 'account', 'choice')
    model = VoteInPoll
    extra = 0
    fields = ['choice', 'account']
    # max_num = Account.objects,active_accounts()

    def get_queryset(self, request):
        qs = super(VoteInPollInline, self).get_queryset(request)
        return qs.select_related('poll', 'account', 'choice')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'choice':
            # kwargs['queryset'] = Choice.objects.filter(poll=Poll.objects.last())
            # import ipdb; ipdb.set_trace()
            kwargs['queryset'] = Choice.objects.filter()
        return super(VoteInPollInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class PollAdmin(admin.ModelAdmin):
    '''
    Admin View for Poll
    '''

    # template
    change_form_template = 'polls/admin/poll_change_form.html'

    # changelist page
    list_display = ('title', 'get_count_votes', 'get_count_choices', 'status', 'date_modified', 'date_added')
    list_filter = ('status', 'date_modified', 'date_added')
    search_fields = ('title',)

    # change page
    form = PollModelForm
    readonly_fields = ('status_changed', 'display_most_popular_choice_or_choices', 'get_count_votes', 'get_count_choices')
    prepopulated_fields = {'slug': ('title', )}
    inlines = [
        ChoiceInline,
        VoteInPollInline,
    ]
    fieldsets = [
        [
            Poll._meta.verbose_name, {
                'fields': [
                    'title',
                    'slug',
                    'status',
                    'status_changed',
                    'display_most_popular_choice_or_choices',
                    'get_count_votes',
                    'get_count_choices',
                ]
            }
        ]
    ]

    def get_queryset(self, request):
        qs = super(PollAdmin, self).get_queryset(request)
        qs = qs.polls_with_count_choices_and_votes()
        return qs

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['chart_poll_result'] = self.build_chart_poll_result()
        return super(PollAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

    def build_chart_poll_result(self):
        # line_chart = settings.PYGAL_CONFIG.Bar()
        pie_chart = pygal.Pie()
        pie_chart.title = 'Browser usage in February 2012 (in %)'
        pie_chart.add('IE', 19.5)
        pie_chart.add('Firefox', 36.6)
        pie_chart.add('Chrome, Chrome, Chrome, Chrome, Chrome, Chrome, Chrome, Chrome, Chrome, Chrome, Chrome, Chrome, ', 36.3)
        pie_chart.add('Safari', 4.5)
        pie_chart.add('Opera', 2.3)
        return pie_chart.render()

    def display_most_popular_choice_or_choices(self, obj):
        most_popular_choice_or_choices = obj.get_most_popular_choice_or_choices()
        if len(most_popular_choice_or_choices) > 1:
            return format_html_join(
                '',
                '<li style="list-style: none;">{0} ({1} votes)</li>',
                (
                    (truncatechars(choice.text_choice, 90), choice.count_votes)
                    for choice in most_popular_choice_or_choices
                ),
            )
        elif len(most_popular_choice_or_choices) == 1:
            popular_choice = most_popular_choice_or_choices[0]
            return format_html(
                _('<p>{0} ({1} votes)</p>'),
                truncatechars(popular_choice.text_choice, 90),
                popular_choice.count_votes,
            )
        else:
            return mark_safe(_('<i>Poll does not have a choices at all.</i>'))
    display_most_popular_choice_or_choices.short_description = _('Most popular choice/choices')


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
    list_select_related = ('poll',)

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

    list_select_related = ('poll', 'account', 'choice')
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
