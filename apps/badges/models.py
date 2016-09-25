
import uuid

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.models_fields import ConfiguredAutoSlugField
from utils.django.models import TimeStampedModel
from utils.django.models_utils import get_admin_url

# from .managers import BadgeManager


class Badge(TimeStampedModel):
    """
    next badge

    top tags
        posts
        score
    """

    BRONZE = 'bronze'
    SILVER = 'silver'
    GOLD = 'gold'

    ANSWERS = 'answers'
    QUESTIONS = 'questions'
    ARTICLES = 'articles'
    SOLUTIONS = 'solutions'
    SNIPPETS = 'snippets'
    POLLS = 'polls'
    FORUMS = 'forums'
    MARKS = 'marks'
    FLAVOURS = 'flavours'
    OPINIONS = 'opinions'
    COMMENTS = 'comments'
    TESTING = 'testing'
    REPLIES = 'replies'
    PROFILE = 'profile'
    OTHER = 'other'

    CHOICES_CATEGORY = (
        (ANSWERS, _('Answers')),
        (QUESTIONS, _('Questions')),
        (ARTICLES, _('Articles')),
        (SOLUTIONS, _('Solutions')),
        (SNIPPETS, _('Snippets')),
        (POLLS, _('Polls')),
        (FORUMS, _('Forums')),
        (MARKS, _('Marks')),
        (FLAVOURS, _('Flavours')),
        (OPINIONS, _('Opinions')),
        (COMMENTS, _('Comments')),
        (TESTING, _('Testing')),
        (REPLIES, _('Replies')),
        (PROFILE, _('Profile')),
        (OTHER, _('Other')),
    )

    CHOICES_KIND = (
        (BRONZE, _('Bronze')),
        (SILVER, _('Silver')),
        (GOLD, _('Gold')),
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(_('Name'), max_length=30, unique=True)
    slug = ConfiguredAutoSlugField(populate_from='name', unique=True)
    description = models.CharField(_('Short description'), max_length=200)
    category = models.CharField(_('Category'), max_length=30, choices=CHOICES_CATEGORY)
    kind = models.CharField(_('Kind'), max_length=20, choices=CHOICES_KIND)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Users'),
        through='GotBadge',
        through_fields=('badge', 'user'),
        # related_name='+',
    )

    objects = models.Manager()
    # objects = BadgeManager()

    class Meta:
        verbose_name = _("Badge")
        verbose_name_plural = _("Badges")
        ordering = ['name']
        get_latest_by = 'created'

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('')

    def get_admin_url(self):
        return get_admin_url(self)

    def get_count_awarded_users(self):
        pass

    def get_count_awarded_users_in_humanreadble_format(self):
        """
        1.2m awarded
        1.5m awarded
        """

        pass


class GotBadge(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('User'),
        on_delete=models.CASCADE, related_name='badges',
    )
    badge = models.ForeignKey(
        'Badge', verbose_name=_('Badge'),
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(_('Date getting'), auto_now_add=True)

    class Meta:
        verbose_name = "Got badge"
        verbose_name_plural = "Got badges"
        ordering = ('-created', )
        get_latest_by = ('created', )
        unique_together = (('user', 'badge'), )
