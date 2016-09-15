
from django.template.defaultfilters import truncatechars
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.utils.html import format_html_join, format_html, conditional_escape
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext
from django.contrib import admin

from utils.django.admin_utils import remove_url_from_admin_urls

from apps.core.admin import AppAdmin, AdminSite

from .models import Poll, Choice, Vote
from .forms import PollAdminModelForm, ChoiceAdminInlineModelForm
from .formsets import ChoiceInlineFormSet
from .actions import make_closed, make_draft, make_opened
from .constants import MIN_COUNT_CHOICES_IN_POLL, MAX_COUNT_CHOICES_IN_POLL
from .apps import PollsConfig
from .listfilters import LatestVotingSimpleListFilter


User = get_user_model()


@AdminSite.register_app_admin_class
class AppAdmin(AppAdmin):

    label = PollsConfig.label

    def get_context_for_tables_of_statistics(self):

        return (
            (
                _('Polls'), (
                    (_('Count polls'), Poll.objects.count()),
                    (_('Average count choices'), Poll.objects.get_avg_count_choices()),
                    (_('Average count votes'), Poll.objects.get_avg_count_votes()),
                    (_('Count opened polls'), Poll.objects.get_count_opened_polls()),
                    (_('Count closed polls'), Poll.objects.get_count_closed_polls()),
                    (_('Count draft polls'), Poll.objects.get_count_draft_polls()),
                ),
            ),
            (
                _('Choices'), (
                    (_('Count choices'), Choice.objects.count()),
                    (_('Average count votes'), Choice.objects.get_avg_count_votes()),
                ),
            ),
            (
                _('Votes'), (
                    (_('Count votes'), Vote.objects.count()),
                    (_('Count distinct voters'), Vote.objects.get_count_distinct_voters()),
                ),
            ),
        )

    def get_context_for_charts_of_statistics(self):

        return (
            {
                'title': _('Chart count votes for the past year'),
                'table': {
                    'fields': (_('Month, year'), _('Count votes')),
                    'data': Vote.objects.get_statistics_count_votes_for_the_past_year(),
                },
                'chart': Vote.objects.get_chart_count_votes_for_the_past_year(),
            },
        )


class ChoiceInline(admin.StackedInline):
    '''
    Stacked Inline View for Choice
    '''

    model = Choice
    form = ChoiceAdminInlineModelForm
    formset = ChoiceInlineFormSet
    min_num = MIN_COUNT_CHOICES_IN_POLL
    max_num = MAX_COUNT_CHOICES_IN_POLL
    extra = 0
    can_delete = True
    list_select_related = ('poll',)
    fields = ('text_choice', 'poll', 'get_count_votes')
    fk_name = 'poll'
    readonly_fields = ('get_count_votes', )


class VoteInline(admin.TabularInline):
    '''
    Stacked Inline View for Choice
    '''

    model = Vote
    extra = 0
    max_num = 0
    can_delete = False
    list_select_related = ('poll', 'choice', 'user')
    fields = ('user', 'get_truncated_text_choice', 'date_voting')
    fk_name = 'poll'
    readonly_fields = ['get_truncated_text_choice', 'user', 'date_voting']


@admin.register(Poll, site=AdminSite)
class PollAdmin(admin.ModelAdmin):
    '''
    Admin View for Poll
    '''

    # templates
    change_form_template = 'polls/admin/poll_change_form.html'

    # changelist
    list_display = (
        'title',
        'get_count_votes',
        'get_count_choices',
        'status',
        'get_date_latest_voting',
        'date_modified',
        'date_added',
    )
    list_filter = (
        'status',
        LatestVotingSimpleListFilter,
        'date_modified',
        'date_added',
    )
    search_fields = ('title',)
    actions = [make_closed, make_draft, make_opened]

    # object
    form = PollAdminModelForm
    readonly_fields = (
        'get_count_choices',
        'get_count_votes',
        'get_date_latest_voting',
        'get_chart_results',
    )
    prepopulated_fields = {'slug': ('title', )}

    def get_queryset(self, request):

        qs = super(PollAdmin, self).get_queryset(request)
        # own annotations
        qs = qs.polls_with_count_choices_and_votes_and_date_lastest_voting()
        return qs

    def get_inline_instances(self, request, obj=None):

        inlines = [ChoiceInline]

        if obj is not None:
            if self.model.objects.get(pk=obj.pk).votes.count():
                inlines.append(VoteInline)
        return [inline(self.model, self.admin_site) for inline in inlines]

    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            (
                Poll._meta.verbose_name, {
                    'fields': (
                        'title',
                        'slug',
                        'status',
                    )
                }
            ),
        ]

        if obj is not None:

            fieldsets.extend((
                (
                    _('Additional information'), {
                        'classes': ('collapse', ),
                        'fields': (
                            'get_count_choices',
                            'get_count_votes',
                            'get_date_latest_voting',
                        )
                    }
                ),
                (
                    _(''), {
                        'classes': ('full-width', ),
                        'fields': ('get_chart_results', )
                    }
                ),
            ))

        return fieldsets

    def suit_cell_attributes(self, obj, column):

        if column in ['get_count_votes', 'get_count_choices', 'status']:
            return {'class': 'text-center'}
        elif column in ['get_date_latest_voting', 'date_modified', 'date_added']:
            return {'class': 'text-right'}

    def suit_row_attributes(self, obj, request):

        if obj.status == Poll.OPENED:
            return {'class': 'success'}
        elif obj.status == Poll.DRAFT:
            return {'class': 'info'}
        elif obj.status == Poll.CLOSED:
            return {'class': 'error'}

    def get_listing_voters_with_admin_url_and_count_votes(self):
        """Return a listing of voters as links to their admin pages, full names and count votes.
        Used in view statistics."""

        # get all voters
        all_voters = User.polls.get_all_voters()

        # if no voters - return corresponding message
        if not all_voters:
            msg = _('No-one yet not participated in polls.')
            return format_html('<i>{0}</i>', msg)

        # else return a listing voters as a links with url to admin_url of a each voter,
        # full name of voter and count votes its
        html_voters = list()
        for voter in all_voters:
            admin_url = voter.get_admin_url()
            voter_full_name = voter.get_full_name()
            count_votes = User.polls.get_count_votes_of_user(voter)

            # make a translatable text for a count votes
            translated_part = ungettext(
                '(%(count_votes)d vote)',
                '(%(count_votes)d votes)',
                count_votes,
            ) % {
                'count_votes': count_votes,
            }

            # pattern for link
            pattern = '<a href="{0}">{1} {2}</a>'.format(admin_url, voter_full_name, translated_part)

            # create html representation for voter and add it to the listing voters,
            # prepared to dislay on page
            html_voter = format_html(pattern, admin_url, voter_full_name, count_votes)
            html_voters.append(html_voter)

        # make join all voters in a safe html
        html_listing_voters = mark_safe(conditional_escape(', ').join(html_voters))
        return html_listing_voters

    def view_preview(self, request):
        """ """

        raise NotImplementedError


@admin.register(Choice, site=AdminSite)
class ChoiceAdmin(admin.ModelAdmin):
    '''
    Admin View for Choice
    '''

    # templates
    #
    # this template is using for preview a choice (all fields is readonly),
    # but using view for change the choice
    # it is easier than write custom view for preview
    change_form_template = 'polls/admin/choice_preview_form.html'

    # changelist
    list_display = ('get_truncated_text_choice', 'poll', 'get_count_votes')
    list_filter = (
        ('poll', admin.RelatedOnlyFieldListFilter),
        # PositiveIntegerRangeListFilter,
    )
    search_fields = ('text_choice',)
    list_select_related = ('poll',)

    # object
    fieldsets = [
        [
            Choice._meta.verbose_name, {
                'fields': [
                    'get_poll_admin_link_as_html',
                    'text_choice',
                    'get_count_votes',
                    'get_voters_with_get_admin_links_as_html',
                ]}
        ]
    ]
    readonly_fields = [
        'get_poll_admin_link_as_html',
        'text_choice',
        'get_count_votes',
        'get_voters_with_get_admin_links_as_html',
    ]

    def get_queryset(self, request):
        qs = super(ChoiceAdmin, self).get_queryset(request)
        qs = qs.choices_with_count_votes()
        return qs

    def suit_cell_attributes(self, obj, column):

        if column == 'get_count_votes':
            return {'class': 'text-center'}

    def suit_row_attributes(self, obj, request):

        if obj in obj.poll.get_most_popular_choice_or_choices():
            return {'class': 'success'}

    def get_voters_with_get_admin_links_as_html(self, obj):
        """Display voters with link to admin url for each user."""

        return format_html_join(
            ', ',
            '<span><a href="{0}">{1}</a></span>',
            ((voter.get_admin_url(), voter.get_full_name()) for voter in obj.get_voters())
        )
    get_voters_with_get_admin_links_as_html.short_description = _('Voters')

    def get_poll_admin_link_as_html(self, obj):
        return format_html('<a href="{0}">{1}</a>', obj.poll.get_admin_url(), obj.poll)
    get_poll_admin_link_as_html.short_description = _('Poll')


@admin.register(Vote, site=AdminSite)
class VoteAdmin(admin.ModelAdmin):
    '''
    Admin View for Vote
    '''

    # objects list
    list_select_related = ('poll', 'user', 'choice')
    list_display = ('truncated_poll', 'user', 'get_truncated_choice', 'date_voting')
    list_filter = (
        ('poll', admin.RelatedOnlyFieldListFilter),
        ('user', admin.RelatedOnlyFieldListFilter),
        ('choice', admin.RelatedOnlyFieldListFilter),
        'date_voting',
    )

    def get_urls(self):

        urls = super().get_urls()

        # remove urls for add and change vote
        remove_url_from_admin_urls(urls, 'add')
        remove_url_from_admin_urls(urls, 'change')
        remove_url_from_admin_urls(urls, 'history')
        remove_url_from_admin_urls(urls, 'delete')

        return urls

    def truncated_poll(self, obj):

        return truncatechars(obj.poll, 100)
    truncated_poll.short_description = Vote._meta.get_field('poll').verbose_name
    truncated_poll.admin_order_field = 'poll'

    def get_truncated_choice(self, obj):

        return truncatechars(obj.choice, 100)
    get_truncated_choice.short_description = Vote._meta.get_field('choice').verbose_name
    get_truncated_choice.admin_order_field = 'choice'

    def suit_cell_attributes(self, obj, column):

        if column == 'date_voting':
            return {'class': 'text-right'}
        elif column == 'user':
            return {'class': 'text-center'}
