
import uuid

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.models import TimeStampedModel
from utils.django.models_utils import get_admin_url

from .managers import BadgeManager, EarnedBadgeManager
from .constants import Badges


class Badge(TimeStampedModel):
    """

    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    name = models.CharField(_('Name'), max_length=50, choices=Badges.CHOICES_NAME)
    description = models.CharField(_('Description'), max_length=50, choices=Badges.CHOICES_DESCRIPTION)
    category = models.CharField(_('Category'), max_length=20, choices=Badges.CHOICES_CATEGORY)
    kind = models.CharField(_('Kind'), max_length=10, choices=Badges.CHOICES_KIND)

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_('Users'),
        through='EarnedBadge',
        through_fields=('badge', 'user'),
        related_name='+',
    )

    objects = models.Manager()
    objects = BadgeManager()

    class Meta:
        verbose_name = _("badge")
        verbose_name_plural = _("badges")
        ordering = ('name', )
        get_latest_by = 'created'
        unique_together = (('name', 'kind'), )

    def __str__(self):

        return '{} badge "{}"'.format(
            self.get_kind_display(),
            self.get_name_display(),
        )

    def get_absolute_url(self):
        return reverse('badges:detail', kwargs={'pk': self.pk, 'name': self.name})

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

    # def check_badge_for_user(self, user):

    #     Notification.objects.create(
    #         user=user,
    #         action=Notification.EARNED_BADGE,
    #         content=_('You earned badge "{}"').format(self),
    #     )


class EarnedBadge(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('User'),
        on_delete=models.CASCADE, related_name='badges',
    )
    badge = models.ForeignKey(
        'Badge', verbose_name=_('Badge'),
        on_delete=models.CASCADE, related_name='+',
    )
    created = models.DateTimeField(_('Date getting'), auto_now_add=True)

    objects = EarnedBadgeManager()

    class Meta:
        verbose_name = "Earned badge"
        verbose_name_plural = "Earned badges"
        ordering = ('-created', )
        get_latest_by = 'created'
        unique_together = (('user', 'badge'), )

    def __str__(self):
        return 'Badge "{0.badge}" of user "{0.user}"'.format(self)
