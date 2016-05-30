
import uuid

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from .validators import validate_url_path
from .managers import VisitManager, DayAttendanceQuerySet


class Visit(models.Model):
    """
    Model for working with visits users the pages.
    Have features keeping users and url visited them.
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
    objects = VisitManager()

    def __str__(self):
        return 'URLPathPage(\'{0.url}\')'.format(self)


class DayAttendance(models.Model):
    """

    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='days_attendances',
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        editable=False,
    )
    day_attendance = models.DateField(_('Day attendance'), editable=False)

    objects = models.Manager()
    objects = DayAttendanceQuerySet.as_manager()

    class Meta:
        db_table = 'days_attendances'
        verbose_name = _('Day attendance')
        verbose_name_plural = _('Days attendances')
        get_latest_by = 'day_attendance'
        ordering = ['day_attendance']
        unique_together = ['user', 'day_attendance']

    objects = models.Manager()
    objects = DayAttendanceQuerySet.as_manager()

    def __str__(self):
        return 'Attendance of user "{0.user}" from {0.day_attendance}'.format(self)
