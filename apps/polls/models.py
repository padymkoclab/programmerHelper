
import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from model_utils.fields import MonitorField, StatusField
from model_utils import Choices

from mylabour.fields_db import ConfiguredAutoSlugField
from mylabour.models import TimeStampedModel
from mylabour.decorators import ClassmethodProperty

from .managers import PollManager, VotesManager
from .querysets import PollQuerySet, ChoiceQuerySet


class Poll(TimeStampedModel):
    """
    Model for poll.
    """

    MIN_COUNT_CHOICES_IN_POLL = 2
    MAX_COUNT_CHOICES_IN_POLL = 10

    CHOICES_STATUS = Choices(
        ('draft', _('Draft')),
        ('opened', _('Opened')),
        ('closed', _('Closed')),
    )

    title = models.CharField(
        _('Title'),
        max_length=200,
        unique=True,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)],
        help_text=_('Allowed from {0} to 200 characters.').format(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)
    )
    description = models.CharField(
        _('Short description'),
        validators=[MinLengthValidator(10)],
        help_text=_('Enter at least 10 characters.'),
        max_length=100,
    )
    slug = ConfiguredAutoSlugField(_('Slug'), populate_from='title', unique=True)
    status = StatusField(verbose_name=_('Status'), choices_name='CHOICES_STATUS', default=CHOICES_STATUS.draft)
    status_changed = MonitorField(_('Date latest status changed'), monitor='status')
    votes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='VoteInPoll',
        through_fields=['poll', 'account'],
        verbose_name=_('Voted users'),
    )

    objects = models.Manager()
    objects = PollManager.from_queryset(PollQuerySet)()

    class Meta:
        db_table = 'polls'
        verbose_name = _("Poll")
        verbose_name_plural = _("Polls")
        ordering = ['date_added']
        get_latest_by = 'date_added'

    def __str__(self):
        return '{0.title}'.format(self)

    def get_absolute_url(self):
        return reverse('polls:poll', kwargs={'pk': self.pk, 'slug': self.slug})

    def get_admin_url(self):
        return reverse(
            'admin:{0}_{1}_change'.format(self._meta.app_label, self._meta.model_name),
            args=(self.pk, )
        )

    def get_most_popular_choice_or_choices(self):
        """Return a most popular choice/choices of that poll, as queryset."""

        # determinating a count votes for choices this poll
        choices_with_count_votes = self.choices.choices_with_count_votes()

        # get max count votes from all choices
        max_count_votes = choices_with_count_votes.aggregate(max_count_votes=models.Max('count_votes'))
        max_count_votes = max_count_votes['max_count_votes']

        # filter choice or choices with max count votes
        choices_with_max_count_votes = choices_with_count_votes.filter(count_votes=max_count_votes)

        return choices_with_max_count_votes

    def get_result_poll(self):
        """Return as a sequnce details about result poll: (Choice, count votes)."""

        # list with pk and count votes
        pks_and_count_votes_need_choices = self.choices.choices_with_count_votes().values_list('id', 'count_votes')

        # replace pk on itself object and return it as tuple
        objects_and_count_votes_need_choices = (
            (self.choices.get(pk=choice_pk), count_votes)
            for choice_pk, count_votes in pks_and_count_votes_need_choices
        )

        return tuple(objects_and_count_votes_need_choices)

    def get_count_votes(self):
        """Return count total votes in poll."""

        return self.votes.count()
    get_count_votes.admin_order_field = 'count_votes'
    get_count_votes.short_description = _('Count votes')

    def get_count_choices(self):
        """Return count choices in poll."""

        return self.choices.count()
    get_count_choices.admin_order_field = 'count_choices'
    get_count_choices.short_description = _('Count choices')

    def get_voters(self):
        """Return users, participated in this poll."""

        return self.votes.all()

    def get_date_lastest_voting(self):
        """Return a datetime latest voting in that poll or None."""

        votes = self.voteinpoll_set
        if votes.count():
            return self.voteinpoll_set.latest().date_voting
    get_date_lastest_voting.admin_order_field = 'date_latest_voting'
    get_date_lastest_voting.short_description = _('Date latest voting')

    @ClassmethodProperty
    @classmethod
    def get_statuses_for_display(cls):
        """ """

        return cls.CHOICES_STATUS._display_map


class Choice(models.Model):
    """
    Model for choice of poll.
    """

    UNIQUE_ERROR_MESSAGE_FOR_TEXT_CHOICE_AND_POLL = _('Poll does not have more than one choice with this text')

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    poll = models.ForeignKey(
        'Poll',
        models.CASCADE,
        verbose_name=_('Poll'),
        related_name='choices',
        limit_choices_to={'status': Poll.CHOICES_STATUS.opened},
    )
    text_choice = models.TextField(_('Text choice'))

    objects = models.Manager()
    objects = ChoiceQuerySet.as_manager()

    class Meta:
        db_table = 'choices'
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")
        ordering = ['poll']
        unique_together = ('poll', 'text_choice')

    def __str__(self):
        return '{0.text_choice}'.format(self)

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('poll', 'text_choice'):
            raise ValidationError(self.UNIQUE_ERROR_MESSAGE_FOR_TEXT_CHOICE_AND_POLL)
        return super(Choice, self).unique_error_message(model_class, unique_check)

    def get_count_votes(self):
        return self.votes.count()
    get_count_votes.short_description = _('Count votes')
    get_count_votes.admin_order_field = 'count_votes'

    def get_voters(self):
        """Return users, participated in this poll."""

        return get_user_model().objects.filter(pk__in=self.votes.values('account'))


class VoteInPoll(models.Model):
    """
    A intermediate model for keeping a choice of a account in certain poll.
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    poll = models.ForeignKey(
        'Poll',
        models.CASCADE,
        verbose_name=_('Poll'),
    )
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name=_('User'),
        related_name='votes',
        limit_choices_to={'is_active': True},
    )
    choice = models.ForeignKey(
        'Choice',
        models.CASCADE,
        verbose_name=_('Choice'),
        related_name='votes',
    )
    date_voting = models.DateTimeField(_('Date voting'), auto_now=True)

    objects = models.Manager()
    objects = VotesManager()

    class Meta:
        db_table = 'votes_in_polls'
        verbose_name = "Vote in poll"
        verbose_name_plural = "Votes in polls"
        ordering = ['poll', 'date_voting']
        get_latest_by = 'date_voting'
        unique_together = ('poll', 'account')

    def __str__(self):
        return _('Vote of a user "{0.account}" in a poll "{0.poll}"').format(self)

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('poll', 'account'):
            return _('This user already participated in that poll.')
        return super(VoteInPoll, self).unique_error_message(model_class, unique_check)
