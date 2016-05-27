
import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings


class BaseGeneric(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('Type object'))
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    date_modified = models.DateTimeField(_('Date modified'), auto_now=True)

    class Meta:
        abstract = True
        get_latest_by = 'date_modified'
        ordering = ['date_modified']

    def is_new(self):
        return self.date_modified > timezone.now() - timezone.timedelta(days=settings.COUNT_DAYS_DISTINGUISH_ELEMENTS_AS_NEW)
    is_new.admin_order_field = 'date_modified'
    is_new.short_description = _('Is new?')
    is_new.boolean = True


class CommentGeneric(BaseGeneric):

    text_comment = models.TextField(_('Text comment'))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Author'),
    )
    date_added = models.DateTimeField(_('Date aded'), auto_now_add=True)

    class Meta(BaseGeneric.Meta):
        db_table = 'comments'
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


class OpinionGeneric(BaseGeneric):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='opinions',
        verbose_name=_('User'),
    )
    is_useful = models.NullBooleanField(_('Is useful?'), default=None)
    is_favorite = models.NullBooleanField(_('Is favorite?'), default=None)

    class Meta(BaseGeneric.Meta):
        db_table = 'opinions'
        verbose_name = _('Opinion')
        verbose_name_plural = _('Opinions')
        permissions = (('can_view_opinions', _('Can view opinions')),)
        unique_together = ['user', 'object_id']

    def clean(self):
        if self.content_object.author == self.user:
            raise ValidationError(_('User not allowed have opinion about hisself labour.'))
        if self.is_useful is None and self.is_favorite is None:
            raise ValidationError(_('User must be given his opinion or share his preference.'))

    def save(self, *args, **kwargs):
        self.clean()
        super(OpinionGeneric, self).save(*args, **kwargs)


class LikeGeneric(BaseGeneric):
    """

    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name=_('User'),
    )
    liked_it = models.BooleanField(_('Liked it?'))

    class Meta(BaseGeneric.Meta):
        db_table = 'likes'
        verbose_name = _('"Like"')
        verbose_name_plural = _('"Likes"')
        permissions = (('can_view_likes', _('Can view likes')),)
        unique_together = ['user', 'object_id']

    def clean(self):
        if self.content_object.author == self.user:
            raise ValidationError(_('User not allowed give his "like" about hisself labour.'))

    def save(self, *args, **kwargs):
        self.clean()
        super(LikeGeneric, self).save(*args, **kwargs)


class ScopeGeneric(BaseGeneric):
    """

    """

    MIN_SCOPE = 0
    MAX_SCOPE = 5

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scopes',
        verbose_name=_('User'),
    )
    scope = models.PositiveSmallIntegerField(_('Scope'), default=MIN_SCOPE, validators=[MaxValueValidator(MAX_SCOPE)])

    class Meta(BaseGeneric.Meta):
        db_table = 'scopes'
        verbose_name = _('Scope')
        verbose_name_plural = _('Scopes')
        permissions = (('can_view_scopes', _('Can view scopes')),)
        unique_together = ['user', 'object_id']

    def clean(self):
        if self.content_object.author == self.user:
            raise ValidationError(_('User not allowed give scope about hisself labour.'))

    def save(self, *args, **kwargs):
        self.clean()
        super(ScopeGeneric, self).save(*args, **kwargs)
