
from django.utils.safestring import mark_safe
from django.template.defaultfilters import truncatechars
from django.utils.html import format_html_join, format_html
from django.template.defaultfilters import truncatewords
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

import pygal

from .models import Poll, Choice, VoteInPoll
from .forms import PollModelForm, ChoiceModelForm, VoteInPollModelForm
from .formsets import ChoiceInlineFormSet


class ChoiceInline(admin.StackedInline):
    '''
    Stacked Inline View for Choice
    '''

    # templates
    template = 'polls/admin/choice_stacked.html'

    # object
    model = Choice
    form = ChoiceModelForm
    formset = ChoiceInlineFormSet
    min_num = Poll.MIN_COUNT_CHOICES_IN_POLL
    max_num = Poll.MAX_COUNT_CHOICES_IN_POLL
    extra = 0
    list_select_related = ('poll',)


class VoteInPollInline(admin.TabularInline):
    '''
    Tabular Inline View for VoteInPoll
    '''

    list_select_related = ('poll', 'account', 'choice')
    model = VoteInPoll
    extra = 0
    fields = ['choice', 'account']
    # max_num = Account.objects,active_accounts()

    def __init__(self, *args, **kwargs):
        super(VoteInPollInline, self).__init__(*args, **kwargs)

    def get_queryset(self, request):
        qs = super(VoteInPollInline, self).get_queryset(request)
        return qs.select_related('poll', 'account', 'choice')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'choice':
            args = request.resolver_match.args
            if args:
                pk = args[0]
                kwargs['queryset'] = Choice.objects.filter(poll__pk=pk)
        return super(VoteInPollInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class PollAdmin(admin.ModelAdmin):
    '''
    Admin View for Poll
    '''

    # template
    change_form_template = 'polls/admin/poll_change_form.html'

    # objects list
    list_display = ('title', 'get_count_votes', 'get_count_choices', 'status', 'date_modified', 'date_added')
    list_filter = ('status', 'date_modified', 'date_added')
    search_fields = ('title',)

    # object
    form = PollModelForm
    readonly_fields = ('status_changed', 'display_most_popular_choice_or_choices', 'get_count_votes', 'get_count_choices')
    prepopulated_fields = {'slug': ('title', )}

    def get_queryset(self, request):

        qs = super(PollAdmin, self).get_queryset(request)

        # add addition annotation for determination count choice and votes for each poll
        qs = qs.polls_with_count_choices_and_votes()

        return qs

    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra_context = extra_context or {}

        # add addition context
        extra_context['chart_poll_result'] = self._build_chart_poll_result(object_id)

        return super(PollAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

    def get_inline_instances(self, request, obj=None):

        self.inlines = [ChoiceInline]

        # add ability CRUD with votes if poll exists and yet not added early
        if obj is not None:
            self.inlines = [ChoiceInline, VoteInPollInline]

        return [inline(self.model, self.admin_site) for inline in self.inlines]

    def get_fieldsets(self, request, obj=None):
        fields = ['title', 'slug', 'status']

        # add additional fields if object already exists
        if obj is not None:
            additional_fields = [
                'status_changed',
                'display_most_popular_choice_or_choices',
                'get_count_votes',
                'get_count_choices',
            ]
            fields.extend(additional_fields)
        return [
            [
                Poll._meta.verbose_name, {'fields': fields}
            ]
        ]

    def _build_chart_poll_result(self, object_id):
        """Return chart as SVG , what reveal result a poll."""

        # chart = pygal.Pie(js=['//kozea.github.io/pygal.js/2.0.x/pygal-tooltips.min.js'])

        # preliminary configuration for chart
        config = pygal.Config()
        config.half_pie = True
        config.legend_at_bottom = True
        config.legend_at_bottom_columns = True
        config.humen_readable = True
        config.half_pie = True
        config.truncate_legend = 65
        config.height = 400
        config.margin_right = 100
        config.margin_left = 100
        config.dynamic_print_values = True
        config.no_data_text = _('Poll does not have votes at all.').format()
        config.style = pygal.style.DefaultStyle(
            value_font_family='googlefont:Raleway',
            value_font_size=5,
            value_label_font_size=5,
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

    def display_most_popular_choice_or_choices(self, obj):
        """Method-wrapper for method get_most_popular_choice_or_choices() of model Poll.
        Return result of the method get_most_popular_choice_or_choices() as humen-readable view HTML."""

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

    # objects list
    list_display = ('__str__', 'poll', 'get_count_votes')
    list_filter = (
        ('poll', admin.RelatedOnlyFieldListFilter),
    )
    search_fields = ('text_choice',)
    list_select_related = ('poll',)

    # object
    fieldsets = [
        [
            Choice._meta.verbose_name, {
                'fields': ['poll', 'text_choice', 'get_count_votes', 'display_voters_with_get_admin_links']
            }
        ]
    ]
    form = ChoiceModelForm
    readonly_fields = ['get_count_votes', 'display_voters_with_get_admin_links']

    def get_queryset(self, request):
        qs = super(ChoiceAdmin, self).get_queryset(request)
        qs = qs.choices_with_count_votes()
        return qs

    def get_fieldsets(self, request, obj=None):

        # basic fields
        fields = ['poll', 'text_choice']

        # if objects already exists, then add new fields
        if obj is not None:
            additional_fields = ['get_count_votes', 'display_voters_with_get_admin_links']
            fields.extend(additional_fields)

        return [
            [
                Choice._meta.verbose_name, {'fields': fields}
            ]
        ]

    def shorted_text_choice(self, obj):
        """Display long text choice as truncated."""

        return truncatewords(obj, 5)

    def display_voters_with_get_admin_links(self, obj):
        """Display voters with link to admin url for each account."""

        voters = obj.get_voters()
        if not voters:
            return mark_safe('<i>Nothing voted for this choice</i>')
        return format_html_join(
            ', ',
            '<span><a href="{0}">{1}</a></span>',
            ((voter.get_admin_url(), voter.get_full_name()) for voter in voters)
        )
    display_voters_with_get_admin_links.short_description = _('Voters')


class VoteInPollAdmin(admin.ModelAdmin):
    '''
    Admin View for VoteInPoll
    '''

    # templates
    change_list_template = 'polls/admin/vote_in_poll_changelist.html'

    # objects list
    list_select_related = ('poll', 'account', 'choice')
    list_display = ('poll', 'account', 'choice', 'date_voting')
    list_filter = (
        ('poll', admin.RelatedOnlyFieldListFilter),
        ('account', admin.RelatedOnlyFieldListFilter),
        'choice',
        'date_voting',
    )

    def get_fieldsets(self, request, obj=None):

        fields = ['poll', 'account', 'choice', 'date_voting']

        # if object does not exists then hide field 'date_voting'
        if obj is None:
            fields = ['poll', 'account', 'choice']

        return [
            [
                VoteInPoll._meta.verbose_name, {'fields': fields}
            ]
        ]

    def get_urls(self):

        urls = super(VoteInPollAdmin, self).get_urls()

        # remove urls for add, change and delete a vote, leaved only url changelist
        urls = list(url for url in urls if url.name == 'polls_voteinpoll_changelist')
        return urls
