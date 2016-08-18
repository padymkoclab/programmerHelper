
import functools

from django.shortcuts import get_object_or_404
from django.conf.urls import url
from django.contrib.auth import get_user_model
from django.apps import apps
from django.template.response import TemplateResponse
from django.http import HttpResponseBadRequest
from django.utils.safestring import mark_safe
from django.utils.html import format_html_join, format_html, conditional_escape
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext
from django.contrib import admin

import pygal

from mylabour.utils import get_statistics_count_objects_by_year, get_latest_or_none

from .models import Poll, Choice, Vote
from .forms import PollModelForm, ChoiceModelForm
from .formsets import ChoiceInlineFormSet
from .actions import make_closed, make_draft, make_opened
from .reports import ExcelReport, PollPDFReport
from .constants import MIN_COUNT_CHOICES_IN_POLL, MAX_COUNT_CHOICES_IN_POLL


User = get_user_model()


# only for admin theme Django-Suit
# it is give feature display menu in left sidebar
def add_current_app_to_request_in_admin_view_for_django_suit(view):
    @functools.wraps(view)
    def wrapped_view(modelAdmin, request, **kwargs):

        request.current_app = 'admin'

        response = view(modelAdmin, request, **kwargs)
        return response
    return wrapped_view


def remove_url_from_admin_urls(urls, url_name):
    for admin_url in urls:
        if admin_url.name == url_name:
            u = admin_url
    urls.remove(u)


class ChoiceInline(admin.StackedInline):
    '''
    Stacked Inline View for Choice
    '''

    model = Choice
    form = ChoiceModelForm
    formset = ChoiceInlineFormSet
    min_num = MIN_COUNT_CHOICES_IN_POLL
    max_num = MAX_COUNT_CHOICES_IN_POLL
    extra = 0
    can_delete = True
    list_select_related = ('poll',)
    fields = ('text_choice', 'poll')
    fk_name = 'poll'


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
        'colored_status_display',
        'get_date_lastest_voting',
        'date_modified',
        'date_added',
    )
    list_filter = ('status', 'date_modified', 'date_added')
    search_fields = ('title',)
    actions = [make_closed, make_draft, make_opened]

    # object
    form = PollModelForm
    readonly_fields = (
        'status_changed',
        'get_most_popular_choice_or_choices_as_html',
        'get_date_lastest_voting',
        'get_count_votes',
        'get_count_choices'
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

    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra_context = extra_context or {}

        # if poll has votes, add in context of view a chart of result of a poll
        poll = get_object_or_404(Poll, pk=object_id)
        if poll.votes.count():
            extra_context['chart_poll_result'] = self._build_chart_poll_result(object_id)

        return super(PollAdmin, self).change_view(request, object_id, form_url, extra_context)

    def get_fieldsets(self, request, obj=None):

        # fields for exists and non exists polls
        fields = ['title', 'slug', 'status']

        # add fields if a poll already exists
        if obj is not None:

            # fields needed for already exists poll
            additional_fields = [
                'status_changed',
                'get_count_votes',
                'get_count_choices',
            ]

            # fields needed if poll has votes
            if obj.votes.count():
                additional_fields.append('get_date_lastest_voting')
                additional_fields.append('get_most_popular_choice_or_choices_as_html')

            fields.extend(additional_fields)
        return [
            [
                Poll._meta.verbose_name, {'fields': fields}
            ]
        ]

    def get_urls(self):

        urls = super(PollAdmin, self).get_urls()

        # create additional urls as django admin`s standart

        # 'polls_poll_preview'
        preview = '{0}_{1}_{2}'.format(self.model._meta.app_label, self.model._meta.model_name, 'preview')
        # 'polls_make_report'
        make_report = '{0}_{1}'.format(self.model._meta.app_label, 'make_report')
        # 'polls_statistics'
        statistics = '{0}_{1}'.format(self.model._meta.app_label, 'statistics')

        # add urls
        additional_urls = [
            url(r'^preview/$', self.admin_site.admin_view(self.view_preview), {}, preview),
            url(r'^make_report/$', self.admin_site.admin_view(self.view_make_report), {}, make_report),
            url(r'^statistics/$', self.admin_site.admin_view(self.view_statistics), {}, statistics), ]

        # additional urls must be placed early standartic urls,
        # since the second will be capture more needed urls
        return additional_urls + urls

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

    def get_most_popular_choice_or_choices_as_html(self, obj):
        """Method-wrapper for method get_most_popular_choice_or_choices() of model Poll.
        Return result of the method get_most_popular_choice_or_choices() as humen-readable view HTML."""

        most_popular_choice_or_choices = obj.get_most_popular_choice_or_choices()

        if len(most_popular_choice_or_choices) > 1:

            lines = list()
            for choice in most_popular_choice_or_choices:
                format_string = ungettext(
                    '%(truncated_text_choice)s (%(count_votes)d vote)',
                    '%(truncated_text_choice)s (%(count_votes)d votes)',
                    choice.count_votes,
                ) % {
                    'count_votes': choice.count_votes,
                    'truncated_text_choice': choice.get_truncated_text_choice()
                }

                line = format_html('<li style="list-style: none;">{0}</li>', format_string)
                lines.append(line)
            return mark_safe(conditional_escape('').join(lines))
        elif len(most_popular_choice_or_choices) == 1:

            popular_choice = most_popular_choice_or_choices[0]

            string = ungettext(
                '%(truncated_text_choice)s (%(count_votes)d vote)',
                '%(truncated_text_choice)s (%(count_votes)d votes)',
                popular_choice.count_votes,
            ) % {
                'truncated_text_choice': popular_choice.get_truncated_text_choice(),
                'count_votes': popular_choice.count_votes,
            }

            return format_html('<li style="list-style: none;">{0}</li>', string)
        else:
            return format_html('<i>{0}</i>', _('Poll does not have a choices at all.'))
    get_most_popular_choice_or_choices_as_html.short_description = _('Most popular choice or choices')

    def colored_status_display(self, obj):
        """ """

        # choice a color
        if obj.status == 'draft':
            color = 'rgb(0, 0, 255)'
        elif obj.status == 'opened':
            color = 'rgb(0, 255, 0)'
        elif obj.status == 'closed':
            color = 'rgb(255, 0, 0)'

        return format_html('<span style="color: {0}">{1}</span>', color, obj.get_status_display())
    colored_status_display.short_description = _('Status')
    colored_status_display.admin_order_field = 'status'

    @add_current_app_to_request_in_admin_view_for_django_suit
    def view_preview(self, request):
        """ """

        raise NotImplementedError

    @add_current_app_to_request_in_admin_view_for_django_suit
    def view_statistics(self, request):
        """Admin view for display statistics about polls, choices, votes and a chart statistics count votes by year"""

        # get a total statistics for the polls, choices and votes
        statistics = {
            'count_polls': Poll.objects.count(),
            'count_opened_polls': Poll.objects.opened_polls().count(),
            'count_closed_polls': Poll.objects.closed_polls().count(),
            'count_draft_polls': Poll.objects.draft_polls().count(),
            'count_choices': Choice.objects.count(),
            'count_votes': Vote.objects.count(),
            'count_voters': Vote.objects.get_count_voters(),
            'all_voters': self.get_listing_voters_with_admin_url_and_count_votes(),
        }

        # add detail about latest changes in polls, if is
        latest_vote = get_latest_or_none(Vote)
        statistics['date_latest_vote'] = getattr(latest_vote, 'date_voting', None)
        statistics['latest_active_poll'] = getattr(latest_vote, 'poll', None)
        statistics['latest_voter'] = getattr(latest_vote, 'user', None)
        statistics['latest_selected_choice'] = getattr(latest_vote, 'choice', None)

        # get a chart statistics of count votes by year
        chart_statistics_count_votes_by_year = self._build_chart_polls_statistics()

        # add a custom context to the view
        # and a context, needed for any admin view
        context = dict(
            self.admin_site.each_context(request),
            title=_('Statistics about polls'),
            statistics=statistics,
            django_admin_media=self.media,
            current_app=apps.get_app_config(Poll._meta.app_label),
            chart_statistics_count_votes_by_year=chart_statistics_count_votes_by_year,
        )

        # return a response, on based a template and passed the context
        return TemplateResponse(request, "polls/admin/statistics.html", context)

    @add_current_app_to_request_in_admin_view_for_django_suit
    def view_make_report(self, request):
        """View for ability of creating an Pdf reports in the admin."""

        # if request`s method is GET,
        # then return simple view for customization creating of Pdf report
        if request.method == 'GET':
            context = dict(
                self.admin_site.each_context(request),
                title=_('Make a report about polls'),
                current_app=apps.get_app_config(Poll._meta.app_label),
                django_admin_media=self.media,
            )
            return TemplateResponse(request, "polls/admin/report.html", context)

        # if request`s method is POST,
        # then Pdf report as file
        elif request.method == 'POST':

            # get type output of report: pdf or excel
            output_report = request.POST.get('output_report', None)

            # get subjects of report
            subjects = [
                request.POST.get('polls', None),
                request.POST.get('choices', None),
                request.POST.get('votes', None),
                request.POST.get('results', None),
                request.POST.get('voters', None),
            ]

            subjects = [subject for subject in subjects if subject]
            if not subjects:
                return HttpResponseBadRequest('Not specified any theme for report.')

            # generate pdf-report by subject
            if output_report == 'report_pdf':
                report = PollPDFReport(request, subjects)

            # generate excel-report
            elif output_report == 'report_excel':
                report = ExcelReport(request, subjects)

            else:
                return HttpResponseBadRequest(_('Type of report is not supplied.'))

            response = report.make_report()
            return response

    def _build_chart_poll_result(self, object_id):
        """Return chart as SVG, what reveal result a poll."""

        # chart configuration
        config = pygal.Config()
        config.half_pie = True
        config.legend_at_bottom = True
        config.legend_at_bottom_columns = True
        config.human_readable = True
        config.half_pie = True
        config.truncate_legend = 80
        config.height = 500
        config.margin_right = 50
        config.margin_left = 50
        config.dynamic_print_values = True
        config.style = pygal.style.DefaultStyle(
            value_font_family='googlefont:Raleway',
            value_font_size=20,
            value_label_font_size=10,
            value_colors=('white',),
            no_data_font_size=11,
        )
        config.tooltip_border_radius = 10

        # create chart
        pie_chart = pygal.Pie(config)
        pie_chart.title = _('Results of the poll').format()

        # add data for chart
        result_poll = Poll.objects.get(pk=object_id).get_result_poll()
        for choice, count_votes in result_poll:
            pie_chart.add(choice.text_choice, count_votes)

        # return chart as SVG
        return pie_chart.render()

    def _build_chart_polls_statistics(self):
        """Return chart in SVG format on based statistics of count votes by year."""

        # get a statistics data by votes
        statistics_count_votes_by_year = get_statistics_count_objects_by_year(Vote, 'date_voting')

        # create a line chart
        chart_statistics_count_votes_by_year = pygal.Line()

        # customization the chart
        chart_statistics_count_votes_by_year.x_label_rotation = 20
        chart_statistics_count_votes_by_year.show_legend = False
        chart_statistics_count_votes_by_year.explicit_size = (1000, 800)
        chart_statistics_count_votes_by_year.title = str(_('Count votes for past year'))
        chart_statistics_count_votes_by_year.x_labels = list(i[0]for i in statistics_count_votes_by_year)

        # add a data to the chart
        chart_statistics_count_votes_by_year.add(
            str(_("Count votes")),
            list(i[1]for i in statistics_count_votes_by_year)
        )

        # return chart in SVG format
        return chart_statistics_count_votes_by_year.render()


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

    def get_urls(self):
        urls = super(ChoiceAdmin, self).get_urls()

        # replace a url`s regex from /change/ to /preview/
        url_polls_choice_change = tuple(url for url in urls if url.name == 'polls_choice_change')[0]
        index_url_polls_choice_change = urls.index(url_polls_choice_change)
        url_polls_choice_view = url(r'^(.+)/preview/$', self.change_view, {}, 'polls_choice_change')
        urls.remove(url_polls_choice_change)
        urls.insert(index_url_polls_choice_change, url_polls_choice_view)

        remove_url_from_admin_urls(urls, 'polls_choice_add')
        remove_url_from_admin_urls(urls, 'polls_choice_history')

        return urls

    def get_voters_with_get_admin_links_as_html(self, obj):
        """Display voters with link to admin url for each user."""

        voters = obj.get_voters()
        if not voters:
            return mark_safe('<i>{0}</i>'.format(_('Nothing voted for this choice.')))
        return format_html_join(
            ', ',
            '<span><a href="{0}">{1}</a></span>',
            ((voter.get_admin_url(), voter.get_full_name()) for voter in voters)
        )
    get_voters_with_get_admin_links_as_html.short_description = _('Voters')

    def get_poll_admin_link_as_html(self, obj):
        return format_html('<a href="{0}">{1}</a>', obj.poll.get_admin_url(), obj.poll)
    get_poll_admin_link_as_html.short_description = _('Poll')


class VoteAdmin(admin.ModelAdmin):
    '''
    Admin View for Vote
    '''

    # objects list
    list_select_related = ('poll', 'user', 'choice')
    list_display = ('poll', 'user', 'choice', 'date_voting')
    list_filter = (
        ('poll', admin.RelatedOnlyFieldListFilter),
        ('user', admin.RelatedOnlyFieldListFilter),
        ('choice', admin.RelatedOnlyFieldListFilter),
        'date_voting',
    )

    def get_urls(self):

        urls = super(VoteAdmin, self).get_urls()

        # remove urls for add and change vote
        remove_url_from_admin_urls(urls, 'polls_vote_add')
        remove_url_from_admin_urls(urls, 'polls_vote_change')

        return urls
