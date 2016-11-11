
import uuid

from django.core.exceptions import ValidationError
# from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings


class Follow(models.Model):
    """

    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, db_index=True,
        related_name='following', verbose_name=_('follower')
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, db_index=True,
        related_name='followers', verbose_name=_('following')
    )
    started = models.DateTimeField(_('started'), auto_now_add=True)

    class Meta:
        verbose_name = _("follow")
        verbose_name_plural = _("follows")
        unique_together = ('follower', 'following')

    def __str__(self):

        return '{0.follower} --> {0.following}'.format(self)

    def clean(self):

        if self.follower == self.following:
            raise ValidationError(_('User not possible following for yourself'))
