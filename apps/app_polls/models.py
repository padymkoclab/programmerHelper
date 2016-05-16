
import uuid

from django.template.defaultfilters import truncatewords
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField
from model_utils.fields import MonitorField, StatusField
from model_utils import Choices
from model_utils.managers import QueryManager

from mylabour.models import TimeStampedModel

from .managers import VoteInPollManager


class Poll(TimeStampedModel):
    """

    """

    MIN_COUNT_CHOICES_IN_POLL = 2
    MAX_COUNT_CHOICES_IN_POLL = 10

    CHOICES_STATUS = Choices(
        ('draft', _('Draft')),
        ('open', _('Open')),
        ('closed', _('Closed')),
    )

    CHOICES_ACCESSABILITY = Choices(
        ('protect', _('Protect')),
        ('public', _('Public')),
    )

    title = models.CharField(
        _('Title'), max_length=200, unique=True, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(_('Slug'), populate_from='title', always_update=True, unique=True, allow_unicode=True, db_index=True)
    accessability = models.CharField(
        _('accessability'),
        max_length=20,
        choices=CHOICES_ACCESSABILITY,
        default=CHOICES_ACCESSABILITY.public,
    )
    status = StatusField(verbose_name=_('status'), choices_name='CHOICES_STATUS', default=CHOICES_STATUS.draft)
    status_changed = MonitorField(_('Status changed'), monitor='status')
    votes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='+',
        through='VoteInPoll',
        through_fields=['poll', 'user'],
        verbose_name=_('Voted users'),
    )

    objects = models.Manager()
    public = QueryManager(accessability=CHOICES_ACCESSABILITY.public)

    class Meta:
        db_table = 'polls'
        verbose_name = _("Poll")
        verbose_name_plural = _("Polls")
        ordering = ['date_added', 'title']
        get_latest_by = 'date_modified'

    def __str__(self):
        return '{0.title}'.format(self)

    def get_absolute_url(self):
        return reverse('app_polls:poll', kwargs={'slug': self.slug})


class Choice(models.Model):
    """

    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    poll = models.ForeignKey(
        'Poll',
        verbose_name=_('Poll'),
        on_delete=models.CASCADE,
        related_name='choices',
    )
    text_choice = models.TextField(_('Text choice'))

    class Meta:
        db_table = 'choices'
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")
        ordering = ['poll']
        unique_together = ['poll', 'text_choice']

    def __str__(self):
        return truncatewords('{0.text_choice}'.format(self), 8)


class VoteInPoll(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    poll = models.ForeignKey(
        'Poll',
        verbose_name=_('Poll'),
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        related_name='votes_in_polls'
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

    def __str__(self):
        return 'Vote of user "{0.user}" in poll "{0.poll}"'.format(self)
