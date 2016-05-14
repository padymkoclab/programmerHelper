
import datetime
import random
import shutil
import uuid

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField
from model_utils import Choices
from model_utils.managers import QueryManager

from apps.app_badges.managers import BadgeManager
from .managers import AccountManager


class AccountLevel(models.Model):
    """

    """

    CHOICES_LEVEL = Choices(
        ('platinum', _('Platinum')),
        ('golden', _('Gold')),
        ('silver', _('Silver')),
        ('diamond', _('Diamond')),
        ('ruby', _('Ruby')),
        ('sapphire', _('Sapphire')),
        ('malachite', _('Malachite')),
        ('amethyst', _('Amethyst')),
        ('emerald', _('Emerald')),
        ('agate', _('Agate')),
        ('turquoise', _('Turquoise')),
        ('amber', _('Amber')),
        ('opal', _('Opal')),
        ('regular', _('Regular')),
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(_('Name'), max_length=50, choices=CHOICES_LEVEL, unique=True)
    slug = AutoSlugField(_('Slug'), populate_from='name', unique=True, always_update=True, allow_unicode=True, db_index=True)
    description = models.TextField(_('Description'))
    color = models.CharField(_('Color'), max_length=50)

    class Meta:
        db_table = 'account_levels'
        verbose_name = _('Level')
        verbose_name_plural = _('Levels')
        ordering = ['name']

    objects = models.Manager()

    def __str__(self):
        return '{0.name}'.format(self)

    def save(self, *args, **kwargs):
        super(AccountLevel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('app_accounts:level', kwargs={'slug': self.slug})


class Account(AbstractBaseUser, PermissionsMixin):
    """
    Custom auth user model with additional fields and username fields as email
    """

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
    level = models.ForeignKey(
        'AccountLevel',
        verbose_name='Level',
        related_name='accounts',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
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
    presents_on_gmail = models.URLField(_('Presents on google services'), blank=True, default='')
    presents_on_github = models.URLField(_('Presents on github'), blank=True, default='')
    presents_on_stackoverflow = models.URLField(_('Presents on stackoverflow'), blank=True, default='')
    personal_website = models.URLField(_('Personal website'), blank=True, default='')
    # private fields
    gender = models.CharField(_('Gender'), max_length=50, choices=CHOICES_GENDER, default=CHOICES_GENDER.vague)
    date_birthday = models.DateField(_('Date birthday'))
    real_name = models.CharField(_('Real name'), max_length=200, default='', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'date_birthday']

    # managers
    objects = models.Manager()
    objects = AccountManager()
    badges_manager = BadgeManager()

    # simple managers
    actives = QueryManager(is_active=True)
    superusers = QueryManager(is_superuser=True)

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
        if self.level is None:
            default_level = AccountLevel.objects.get(name=AccountLevel.CHOICES_LEVEL.regular)
            self.level = default_level
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

    def get_reputation(self):
        pass

    def last_seen(self):
        # Last seen 11 mins ago
        pass

    def last_activity(self):
        pass

    def get_activity(self):
        pass


class AccountView(models.Model):
    """

    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    account_viewer = models.ForeignKey(
        'Account',
        related_name='as_viewer',
        on_delete=models.CASCADE,
    )
    account_viewed = models.ForeignKey(
        'Account',
        related_name='as_viewed',
        on_delete=models.CASCADE,
    )
    date_view = models.DateTimeField(_('Date view'), auto_now_add=True)

    class Meta:
        db_table = 'account_views'
        verbose_name = _('View')
        verbose_name_plural = _('Views')
        get_latest_by = 'date_view'
        ordering = ['date_view']
        unique_together = ['account_viewer', 'account_viewed']

    objects = models.Manager()

    def __str__(self):
        return 'View account {0.account_viewed}'.format(self)

    def clean(self):
        if self.account_viewed == self.account_viewer:
            raise ValidationError({
                '__all__': _('Same account impossible will be viewer and viewed.')
            })
