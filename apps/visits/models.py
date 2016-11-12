
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.datetime_utils import convert_date_to_django_date_format
from utils.django.models import UUIDable, Updateable, Viewable

from .validators import validate_comma_separated_objects_list
from .managers import VisitPageManager, AttendanceManager, VisitUserBrowserManager, VisitUserSystemManager


class VisitPage(UUIDable, Viewable):
    """
    Model for working with visits users of pages.
    Have features keeping users and url visited them.
    """

    url = models.CharField(_('URL'), validators=[], max_length=1000, unique=True)

    class Meta:
        verbose_name = _('visit page')
        verbose_name_plural = _('visits page')

    objects = models.Manager()
    objects = VisitPageManager()

    def __str__(self):
        return '{0.url}'.format(self)


class Attendance(UUIDable):
    """
    Model for keep days of attendance of website whole
    """

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='attendances',
        verbose_name=_('user'), editable=False,
    )
    date = models.DateField(
        _('date'), editable=False, auto_now_add=True,
        db_index=True, unique=True, error_messages={
            'unique': _('Attendance on this day already exists')
        }
    )

    objects = models.Manager()
    objects = AttendanceManager()

    class Meta:
        verbose_name = _('visit site')
        verbose_name_plural = _('visits site')
        get_latest_by = 'date'
        ordering = ('-date', )

    def __str__(self):

        return convert_date_to_django_date_format(self.date)

    def get_count_visitors(self):

        return self.users.count()
    get_count_visitors.short_description = _('Count visitors')
    get_count_visitors.admin_order_field = 'count_visitors'


class Visit(UUIDable, Updateable):
    """
    Model for keep latest visit of the site
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='last_seen',
        verbose_name=_('user'), editable=False, db_index=True
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _('visit')
        verbose_name_plural = _('visits')
        get_latest_by = 'updated'
        ordering = ('-updated', )

    def __str__(self):
        return '{0.user}'.format(self)


class VisitUserBrowser(UUIDable):
    """
    For only registered users
    """

    name = models.CharField(_('name'), max_length=100, unique=True)
    user_pks = models.TextField(
        _('primary key of users'), validators=[validate_comma_separated_objects_list],
        default='', blank=True
    )

    objects = models.Manager()
    objects = VisitUserBrowserManager()

    class Meta:
        verbose_name = _('browser')
        verbose_name_plural = _('browsers')
        ordering = ('-name', )

    def __str__(self):
        return '{0.name}'.format(self)


class VisitUserSystem(UUIDable):
    """
    For only registered users
    """

    name = models.CharField(_('name'), max_length=50, unique=True)
    user_pks = models.TextField(
        _('primary key of users'), validators=[validate_comma_separated_objects_list],
        default='', blank=True
    )

    objects = models.Manager()
    objects = VisitUserSystemManager()

    class Meta:
        verbose_name = _('operation system')
        verbose_name_plural = _('operation systems')
        ordering = ('-name', )

    def __str__(self):
        return '{0.name}'.format(self)
