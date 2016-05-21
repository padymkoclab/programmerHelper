
import uuid

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from .validators import validate_url_path


class Visit(models.Model):
    """

    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    url = models.CharField(_('Path URL'), validators=[validate_url_path], max_length=1000, unique=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('users'),
        related_name='+',
    )

    class Meta:
        db_table = 'visits'
        verbose_name = _('Visit')
        verbose_name_plural = _('Visits')

    objects = models.Manager()

    def __str__(self):
        return 'URLPathPage(\'{0.url}\')'.format(self)
