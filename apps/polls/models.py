
import itertools
import uuid

from django.template.defaultfilters import truncatechars
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from mylabour.datetime_utils import convert_date_to_django_date_format
from mylabour.models_fields import ConfiguredAutoSlugField
from mylabour.models import TimeStampedModel

from .managers import PollManager, VoteManager
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
        help_text=_('Allowed from {0} to 200 characters.').format(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)
    )
    description = models.CharField(
        _('Short description'),
        validators=[MinLengthValidator(10)],
        help_text=_('Enter at least 10 characters.'),
        max_length=100,
    )
    slug = ConfiguredAutoSlugField(_('Slug'), populate_from='title', unique=True)
    status = models.CharField(_('Status'), max_length=10, choices=CHOICES_STATUS, default=DRAFT)
    voters = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Vote',
        through_fields=['poll', 'user'],
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

        # filter choice or choices with max count votes
        choices_with_max_count_votes = choices_with_count_votes.filter(count_votes=max_count_votes)

        return choices_with_max_count_votes

    def get_result_poll(self):
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

        return self.voters.all()

    def get_date_lastest_voting(self):
        """Return a datetime latest voting, in the project datetime format, of the poll or none."""

        try:
            # get date voting of a latest vote, if exists
            date_voting = self.votes.latest().date_voting

            # convert and to return the datetime object to the project datetime format
            date_voting = convert_date_to_django_date_format(date_voting)
            return date_voting
        except Vote.DoesNotExist:
            return
    get_date_lastest_voting.admin_order_field = 'date_latest_voting'
    get_date_lastest_voting.short_description = _('Date latest voting')


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
        limit_choices_to={'status': Poll.OPENED},
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
        'Poll',
        models.CASCADE,
        verbose_name=_('Poll'),
        related_name='votes',
    )
    user = models.ForeignKey(
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
    objects = VoteManager()

    class Meta:
        db_table = 'votes'
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
        ordering = ['poll', '-date_voting']
        get_latest_by = 'date_voting'
        unique_together = ('poll', 'user')

    def __str__(self):
        return _('Vote of a user "{0.user}" in a poll "{0.poll}"').format(self)

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
