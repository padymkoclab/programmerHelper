
import uuid

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from .validators import validate_comma_separated_objects_list
from .managers import VisitPageManager, AttendanceManager, VisitUserBrowserManager, VisitUserSystemManager


class VisitPage(models.Model):
    """
    Model for working with visits users of pages.
    Have features keeping users and url visited them.
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    url = models.CharField(_('URL'), validators=[], max_length=1000, unique=True)
    count = models.IntegerField(_('count visits'), default=0)

    class Meta:
        verbose_name = _('visit page')
        verbose_name_plural = _('visits page')

    objects = models.Manager()
    objects = VisitPageManager()

    def __str__(self):
        return '{0.url}'.format(self)


class VisitSite(models.Model):
    """
    Model for keep days of attendance of website whole
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='attendances',
        verbose_name=_('user'),
        editable=False,
    )
    date = models.DateField(_('date'), editable=False, auto_now_add=True, unique=True, error_messages={
        'unique': _('Attendance on this day already exists')
    })

    objects = models.Manager()
    objects = AttendanceManager()

    class Meta:
        verbose_name = _('visit site')
        verbose_name_plural = _('visits site')
        get_latest_by = 'date'
        ordering = ('-date', )

    def __str__(self):
        return '{0.date}'.format(self)


class Visit(models.Model):
    """
    Model for keep latest visit of the site
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='last_seen',
        verbose_name=_('user'),
        editable=False,
    )
    date = models.DateTimeField(_('date'), editable=False)

    objects = models.Manager()

    class Meta:
        verbose_name = _('visit')
        verbose_name_plural = _('visits')
        get_latest_by = 'date'
        ordering = ('-date', )

    def __str__(self):
        return '{0.user}'.format(self)


class VisitUserBrowser(models.Model):
    """
    For only registered users
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
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


class VisitUserSystem(models.Model):
    """
    For only registered users
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
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
