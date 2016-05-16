
import uuid

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField

# from .managers import BadgeManager


class Badge(models.Model):
    """
    next badge

    top tags
        posts
        score
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(_('Name'), max_length=30, unique=True)
    slug = AutoSlugField(_('Slug'), populate_from='name', unique=True, always_update=True, allow_unicode=True, db_index=True)
    short_description = models.CharField(_('Short description'), max_length=100)
    date_created = models.DateTimeField(_('Date created'), auto_now_add=True)
    # weight
    # type
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Users'),
        through='GettingBadge',
        through_fields=('badge', 'user'),
        related_name='+',
    )

    objects = models.Manager()
    # objects = BadgeManager()

    class Meta:
        db_table = 'badges'
        verbose_name = _("Badge")
        verbose_name_plural = _("Badges")
        ordering = ['name']
        get_latest_by = 'date_created'

    def __str__(self):
        return '{0.name}'.format(self)


class GettingBadge(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        related_name='badges',
    )
    badge = models.ForeignKey('Badge', verbose_name=_('Badge'), on_delete=models.CASCADE, related_name='+')
    conditions = models.TextField(_('Pleasurable conditions'))
    # reasons
    date_getting = models.DateTimeField(_('Date getting'), auto_now_add=True)

    class Meta:
        db_table = 'getting_badges'
        verbose_name = "Getting badge"
        verbose_name_plural = "Getting badges"
        ordering = ['-date_getting']
        get_latest_by = 'date_getting'
        unique_together = ['user', 'badge']

    def __str__(self):
        return 'Badge "{0.badge}" of user {0.user}'.format(self)

    @staticmethod
    def normalize_conditions(list_conditions):
        # if not isinstance(list_conditions, (tuple, list)):
        #     raise TypeError('Please transfer sequence.')
        return ', '.join(i.__str__() for i in list_conditions)
