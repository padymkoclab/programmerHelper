
from django.utils import timezone
from django.contrib.sessions.base_session import AbstractBaseSession
# from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
# from django.conf import settings

from apps.app_sessions.backends.extended_session_store import SessionStore


class ExtendedSession(AbstractBaseSession):
    """
    Extended and enhanced build-in in Django application for sessions.
    Addionaly storing account and session detail, as well as have several useful methods.
    """

    account_pk = models.UUIDField(null=True, db_index=True)
    # device
    # location
    # ip_address
    # last activity
    # GeoIP

    class Meta:
        db_table = 'extended_sessions'
        verbose_name = _('Session')
        verbose_name_plural = _('Sessions')
        app_label = 'app_sessions'
        # get_latest_by = 'date_'
        ordering = ['-expire_date']
        # unique_together = ['', '']

    # objects = models.Manager()

    # def __str__(self):
    #     return '{0.name}'.format(self)

    # def save(self, *args, **kwargs):
    #     super(ExtendedSession, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('app_:', kwargs={'slug': self.slug})

    @classmethod
    def get_session_store_class(cls):
        return SessionStore

    def status_session(self):
        """Check up session on status as valid. May be expired or active."""
        return self.expire_date > timezone.now()
    status_session.short_description = _('Status')
    status_session.admin_order_field = 'expire_date'
    status_session.boolean = True

    # def get_decoded(self):
    #     return self
