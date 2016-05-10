
import datetime
import random
import shutil
import uuid

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.conf import settings

from model_utils import Choices
from model_utils.managers import QueryManager

from apps.app_badges.models import Badge, GettingBadge
from apps.app_badges.managers import BadgeManager
from .managers import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    """
    Custom auth user model with additional fields and username fields as email
    """

    CHOICES_ACCOUNT_TYPES = Choices(
        ('regular', _('Regular')),
        ('golden', _('Golden')),
        ('platinum', _('Platinum')),
    )

    CHOICES_GENDER = Choices(
        ('vague', _('Vague')),
        ('man', _('Man')),
        ('woman', _('Woman')),
    )

    PATH_TO_ACCOUNT_DEFAULT_PICTURES = str(settings.STATIC_ROOT) + '/app_accounts/images/avatar_pictures_default/'

    def limit_choices_badges():
        return {'pub_date__lte': datetime.date.utcnow()}

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # account detail
    email = models.EmailField(
            _('Email'),
            unique=True,
            error_messages={
                'unique': _('Account with this email already exists.')
            }
    )
    username = models.CharField(_('Username'), max_length=200, help_text=_('Displayed name'))
    is_active = models.BooleanField(_('Is active'), default=True, help_text=_('Designated that this user is not disabled.'))
    profile_views = models.IntegerField(_('Profile views'), default=0, editable=False)
    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True)
    account_type = models.CharField(
        _('Type of account'),
        max_length=50,
        choices=CHOICES_ACCOUNT_TYPES,
        default=CHOICES_ACCOUNT_TYPES.regular,
        editable=False,
    )
    picture = models.FilePathField(
        path=PATH_TO_ACCOUNT_DEFAULT_PICTURES,
        match='.*',
        recursive=True,
        verbose_name=_('Picture'),
        max_length=200,
        blank=True,
        allow_folders=False,
        allow_files=True,
    )
    # presents in web
    presents_on_gmail = models.URLField(_('Presents on google services'), blank=True)
    presents_on_github = models.URLField(_('Presents on github'), blank=True)
    presents_on_stackoverflow = models.URLField(_('Presents on stackoverflow'), blank=True)
    personal_website = models.URLField(_('Personal website'), blank=True)
    # badges
    badges = models.ManyToManyField(
        Badge,
        related_name='users',
        verbose_name=_('Badges'),
        through=GettingBadge,
        through_fields=('account', 'badge'),
    )
    # private fields
    gender = models.CharField(_('Gender'), max_length=50, choices=CHOICES_GENDER, default=CHOICES_GENDER.vague)
    date_birthday = models.DateField(_('Date birthday'))
    real_name = models.CharField(_('Real name'), max_length=200, default='', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'date_birthday']

    # managers
    objects = models.Manager()
    objects = AccountManager()
    badges_checker = BadgeManager()
    # simple managers
    active_accounts = QueryManager(is_active=True)
    superuser_accounts = QueryManager(is_superuser=True)

    class Meta:
        db_table = 'account'
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        ordering = ['-last_login']  # not worked
        get_latest_by = 'date_joined'

    def __str__(self):
        return '{0.email}'.format(self)

    def save(self, *args, **kwargs):
        if not self.picture:
            files = shutil.os.listdir(self.PATH_TO_ACCOUNT_DEFAULT_PICTURES)
            if files:
                self.picture = self.PATH_TO_ACCOUNT_DEFAULT_PICTURES + random.choice(files)
        super(Account, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('app_accounts:detail', kwargs={'account_email': self.email})

    def get_full_name(self):
        return '{0.username} ({0.email})'.format(self)

    def get_short_name(self):
        return '{0.email}'.format(self)

    @property
    def is_staff(self):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # Member for 56 days

    # visited 42 days, 5 consecutive

    # Last seen 11 mins ago

    # last activity

    """
    activity
    account_detail
    account change

    user feed
    location GeoDjango

    questions sorted by votes, activity, newest
    answers sorted by votes, activity, newest

    3 profile views

    """

    def get_reputation(self):
        pass

    def get_badges(self):
        pass
