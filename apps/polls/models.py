
import itertools
import uuid

from django.template import Context, Template
from django.utils.html import mark_safe, escape, format_html
from django.template.defaultfilters import truncatechars
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

import pygal

from utils.django.models_utils import get_admin_url
from utils.django.datetime_utils import convert_date_to_django_date_format
from utils.django.models_fields import ConfiguredAutoSlugField
from utils.django.models import TimeStampedModel

from .managers import PollManager, ChoiceManager, VoteManager
from .querysets import PollQuerySet, ChoiceQuerySet


class Poll(TimeStampedModel):
    """
    Model for poll.
    """

    DRAFT = 'DRAFT'
    OPENED = 'OPENED'
    CLOSED = 'CLOSED'

    CHOICES_STATUS = (
        (DRAFT, _('Draft')),
        (OPENED, _('Opened')),
        (CLOSED, _('Closed')),
    )

    title = models.CharField(
        _('Title'), max_length=200, unique=True,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)],
    )
    description = models.CharField(
        _('Short description'),
        validators=[MinLengthValidator(10)],
        max_length=100,
    )
    slug = ConfiguredAutoSlugField(populate_from='title', unique=True)
    status = models.CharField(_('Status'), max_length=10, choices=CHOICES_STATUS, default=DRAFT)
    # deactivate_date = models.DateTimeField(null=True, blank=True,
    #     help_text=_("Point of time after this poll would be automatic deactivated"),
    # )
    voters = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Vote',
        through_fields=['poll', 'user'],
        verbose_name=_('Voters'),
    )

    objects = models.Manager()
    objects = PollManager.from_queryset(PollQuerySet)()

    class Meta:
        verbose_name = _("Poll")
        verbose_name_plural = _("Polls")
        ordering = ['created']
        get_latest_by = 'created'

    def __str__(self):
        return '{0.title}'.format(self)

    def get_absolute_url(self):
        return reverse('polls:poll', kwargs={'pk': self.pk, 'slug': self.slug})

    def get_admin_url(self):
        return get_admin_url(self)

    def natural_key(self):
        return self.title
    natural_key.dependencies = ['users.User']

    def get_most_popular_choice_or_choices(self):
        """Return a most popular choice/choices of that poll, as queryset."""

        # determinating a count votes for choices this poll
        choices_with_count_votes = self.choices.choices_with_count_votes()

        # get max count votes from all choices
        max_count_votes = choices_with_count_votes.aggregate(max_count_votes=models.Max('count_votes'))
        max_count_votes = max_count_votes['max_count_votes']

        if max_count_votes == 0:
            return []

        # filter choice or choices with max count votes
        choices_with_max_count_votes = choices_with_count_votes.filter(count_votes=max_count_votes)

        return choices_with_max_count_votes

    def get_result(self):
        """Return as a sequnce details about result poll: (Choice, count votes)."""

        # determinate count votes in each choices
        # and make an order of choices by descending
        choices_with_count_votes = self.choices.choices_with_count_votes().order_by('-count_votes')

        # get count votes of an each choice
        count_votes_of_choices = choices_with_count_votes.values_list('count_votes')

        # make as flatten list
        count_votes_of_choices = itertools.chain.from_iterable(count_votes_of_choices)

        # make two-nested list: (choice, count_votes)
        result = zip(choices_with_count_votes, count_votes_of_choices)

        # convert generator to tuple and to return it
        return tuple(result)

    def get_count_votes(self):
        """Return count total votes in poll."""

        if hasattr(self, 'count_votes'):
            return self.count_votes

        return self.votes.count()
    get_count_votes.admin_order_field = 'count_votes'
    get_count_votes.short_description = _('Count votes')

    def get_count_choices(self):
        """Return count choices in poll."""

        if hasattr(self, 'count_choices'):
            return self.count_choices

        return self.choices.count()
    get_count_choices.admin_order_field = 'count_choices'
    get_count_choices.short_description = _('Count choices')

    def get_voters(self):
        """Return users, participated in this poll."""

        return self.voters.all()

    def get_date_latest_voting(self):
        """Return a datetime latest voting, in the project datetime format, of the poll or none."""

        if hasattr(self, 'date_latest_voting'):
            return self.date_latest_voting

        if self.votes.exists():
            return self.votes.latest().created
        return
            # convert and to return the datetime object to the project datetime format
            # created = convert_date_to_django_date_format(created)
    get_date_latest_voting.admin_order_field = 'date_latest_voting'
    get_date_latest_voting.short_description = _('Date latest voting')

    def get_chart_results(self):
        """ """

        config = pygal.Config()
        config.half_pie = True

        chart = pygal.Pie(config)

        chart.add('IE', 19.5)
        chart.add('Firefox', 36.6)
        chart.add('Chrome', 36.3)
        chart.add('Safari', 4.5)
        chart.add('Opera', 2.3)

        svg = chart.render()

        svg = mark_safe(svg)
        # svg = mark_safe(Template('{{ svg|safe }}').render(Context({'svg': svg})))
        return format_html('{}', svg)


class Choice(models.Model):
    """
    Model for choice of poll.
    """

    UNIQUE_ERROR_MESSAGE_FOR_TEXT_CHOICE_AND_POLL = _('Poll does not have more than one choice with this text')

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    poll = models.ForeignKey(
        'Poll', verbose_name=_('Poll'),
        on_delete=models.CASCADE, related_name='choices',
    )
    text_choice = models.TextField(_('Text choice'))

    objects = models.Manager()
    objects = ChoiceManager.from_queryset(ChoiceQuerySet)()

    class Meta:
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")
        ordering = ['poll']
        unique_together = ('poll', 'text_choice')

    def __str__(self):
        return '{0.text_choice}'.format(self)

    def unique_error_message(self, model_class, unique_check):
        """A custom text for fields in meta-attribute unique_together."""

        if model_class == type(self) and unique_check == ('poll', 'text_choice'):
            raise ValidationError(self.UNIQUE_ERROR_MESSAGE_FOR_TEXT_CHOICE_AND_POLL)
        return super(Choice, self).unique_error_message(model_class, unique_check)

    def natural_key(self):
        return (self.poll.natural_key(), self.text_choice)
    natural_key.dependencies = ['polls.Poll']

    def get_count_votes(self):
        return self.votes.count()
    get_count_votes.short_description = _('Count votes')
    get_count_votes.admin_order_field = 'count_votes'

    def get_voters(self):
        """Return users, participated in this poll."""

        return get_user_model().objects.filter(pk__in=self.votes.values('user'))

    def get_truncated_text_choice(self):
        return truncatechars(self.text_choice, 90)
    get_truncated_text_choice.admin_order_field = 'text_choice'
    get_truncated_text_choice.short_description = _('Text choice')


class Vote(models.Model):
    """
    Model of vote. This model is intermediate model for keeping a choice of a user in certain poll.
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    poll = models.ForeignKey(
        'Poll', models.CASCADE,
        verbose_name=_('Poll'), related_name='votes',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE,
        verbose_name=_('User'), related_name='votes',
    )
    choice = models.ForeignKey(
        'Choice',
        models.CASCADE,
        verbose_name=_('Choice'),
        related_name='votes',
    )
    created = models.DateTimeField(_('Date added'), auto_now_add=True)

    objects = models.Manager()
    objects = VoteManager()

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
        ordering = ['-created']
        get_latest_by = 'created'
        unique_together = ('poll', 'user')

    def __str__(self):
        return _('In a poll "{0.poll}"').format(self)

    def unique_error_message(self, model_class, unique_check):
        """A custom text for fields in meta-attribute unique_together."""

        if model_class == type(self) and unique_check == ('poll', 'user'):
            return _('This user already participated in that poll.')
        return super(Vote, self).unique_error_message(model_class, unique_check)

    def get_truncated_text_choice(self):
        """Return a truncated text choice of a current choice. Using in admin."""

        return truncatechars(self.choice.text_choice, 70)
    get_truncated_text_choice.short_description = Choice._meta.verbose_name

    def natural_key(self):
        return (self.poll.natural_key(), self.user.natural_key(), self.choice.natural_key())
    natural_key.dependencies = [
        'users.User',
        'polls.Choice',
        'polls.Poll',
    ]
