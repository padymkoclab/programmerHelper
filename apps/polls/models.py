
import uuid

from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from model_utils.fields import MonitorField, StatusField
from model_utils import Choices

from mylabour.fields_db import ConfiguredAutoSlugField
from mylabour.models import TimeStampedModel
from mylabour.validators import MinCountWordsValidator

from .managers import PollManager, OpendedPollManager, VoteInPollManager
from .querysets import PollQuerySet


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
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    description = models.CharField(
        _('Short description'),
        validators=[MinCountWordsValidator(5)],
        help_text=_('Enter at least 5 words.'),
        max_length=100,
    )
    slug = ConfiguredAutoSlugField(_('Slug'), populate_from='title', unique=True)
    status = StatusField(verbose_name=_('status'), choices_name='CHOICES_STATUS', default=CHOICES_STATUS.draft)
    status_changed = MonitorField(_('Status changed'), monitor='status')
    votes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='+',
        through='VoteInPoll',
        through_fields=['poll', 'account'],
        verbose_name=_('Voted users'),
    )

    objects = models.Manager()
    objects = PollManager.from_queryset(PollQuerySet)()
    draft = models.Manager()
    opened = OpendedPollManager()
    closed = models.Manager()

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
            args=(self.pk,)
        )


class Choice(models.Model):
    """
    Model for choice of poll.
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    poll = models.ForeignKey(
        'Poll',
        verbose_name=_('Poll'),
        on_delete=models.CASCADE,
        related_name='choices',
        limit_choices_to={'status': Poll.CHOICES_STATUS.opened},
    )
    text_choice = models.TextField(_('Text choice'))

    class Meta:
        db_table = 'choices'
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")
        ordering = ['poll']
        unique_together = ['poll', 'text_choice']

    def __str__(self):
        return '{0.text_choice}'.format(self)


class VoteInPoll(models.Model):
    """
    A intermediate model for keeping a choice of a account in certain poll.
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    poll = models.ForeignKey(
        'Poll',
        verbose_name=_('Poll'),
        on_delete=models.CASCADE,
    )
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        related_name='votes_in_polls',
        limit_choices_to={'is_active': True},
    )
    choice = models.ForeignKey(
        'Choice',
        verbose_name=_('Choice'),
        on_delete=models.CASCADE,
        related_name='votes',
    )
    date_voting = models.DateTimeField(_('Date voting'), auto_now=True)

    objects = models.Manager()
    objects = VoteInPollManager()

    class Meta:
        db_table = 'votes_in_polls'
        verbose_name = "Vote in poll"
        verbose_name_plural = "Votes in poll"
        ordering = ['poll', 'date_voting']
        get_latest_by = 'date_voting'
        unique_together = ('poll', 'account')

    def __str__(self):
        return _('Vote of a user "{0.account}" in a poll "{0.poll}"').format(self)
