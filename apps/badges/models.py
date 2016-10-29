
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

    name = models.CharField(_('Name'), max_length=50, choices=Badges.CHOICES_NAME, db_index=True)
    description = models.CharField(_('Description'), max_length=50, choices=Badges.CHOICES_DESCRIPTION, db_index=True)
    category = models.CharField(_('Category'), max_length=20, choices=Badges.CHOICES_CATEGORY, db_index=True)
    kind = models.CharField(_('Kind'), max_length=10, choices=Badges.CHOICES_KIND, db_index=True)

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

        return '{} ({})'.format(
            self.get_name_display(),
            self.get_kind_display().lower(),
        )

    def get_absolute_url(self):
        return reverse('badges:detail', kwargs={'pk': self.pk, 'name': self.name})

    def get_admin_url(self):
        return get_admin_url(self)

    def get_count_awarded_users(self):

        return self.earned.count()
    get_count_awarded_users.short_description = _('Count awarded users')
    get_count_awarded_users.admin_order_field = 'count_awarded_userst'

    def get_count_awarded_users_in_humanreadble_format(self):
        """
        1.2m awarded
        1.5m awarded
        """

        pass

    def get_date_latest_awarded(self):

        if self.earned.exists():
            return self.earned.latest().created
        return

    get_date_latest_awarded.short_description = _('Date latest awarded')
    get_date_latest_awarded.admin_order_field = 'date_latest_awarded'

    def get_lastest_awarded_user(self):

        if self.earned.exists():
            return self.earned.latest().user
        return

    get_lastest_awarded_user.short_description = _('Lastest awarded user')
    get_lastest_awarded_user.admin_order_field = 'lastest_awarded_user'

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
        db_index=True
    )
    badge = models.ForeignKey(
        'Badge', verbose_name=_('Badge'),
        on_delete=models.CASCADE, related_name='earned',
        db_index=True
    )
    created = models.DateTimeField(_('Date getting'), auto_now_add=True, db_index=True)

    objects = EarnedBadgeManager()

    class Meta:
        verbose_name = "Earned badge"
        verbose_name_plural = "Earned badges"
        ordering = ('-created', )
        get_latest_by = 'created'
        unique_together = (('user', 'badge'), )

    def __str__(self):
        return 'Badge "{0.badge}" of user "{0.user}"'.format(self)
