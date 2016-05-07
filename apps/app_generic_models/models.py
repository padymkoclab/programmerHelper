
import uuid

from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from model_utils import Choices


class BaseGeneric(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
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


class UserComment_Generic(BaseGeneric):

    text_comment = models.TextField(_('Text comment'))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name='comments',
        verbose_name=_('Author'),
    )
    date_added = models.DateTimeField(_('Date aded'), auto_now_add=True)

    class Meta(BaseGeneric.Meta):
        db_table = 'comments'
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


class UserOpinion_Generic(BaseGeneric):

    CHOICES_FAVORITE = Choices(
        ('yes', _('Yes')),
        ('unknown', _('Unknown')),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name='opinions',
        verbose_name=_('User'),
    )
    is_useful = models.NullBooleanField(_('Is was useful for you?'))
    is_favorite = models.CharField(
        _('Is your favorite theme?'),
        max_length=30,
        choices=CHOICES_FAVORITE,
        default=CHOICES_FAVORITE.unknown,
    )

    class Meta(BaseGeneric.Meta):
        db_table = 'opinions'
        verbose_name = _('Opinion')
        verbose_name_plural = _('Opinions')
        permissions = (('can_view_opinions', _('Can view opinions')),)

    def display_is_favorite_as_boolean(self):
        if self.is_favorite == self.CHOICES_FAVORITE.yes:
            return True
        if self.is_favorite == self.CHOICES_FAVORITE.unknown:
            return None
    display_is_favorite_as_boolean.boolean = True
    display_is_favorite_as_boolean.admin_order_field = 'is_favorite'
    display_is_favorite_as_boolean.short_description = _('Is favorite')


class UserLike_Generic(BaseGeneric):
    """

    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name='likes',
        verbose_name=_('User'),
    )
    liked_it = models.BooleanField(_('Liked it?'))

    class Meta(BaseGeneric.Meta):
        db_table = 'likes'
        verbose_name = _('"Like"')
        verbose_name_plural = _('"Likes"')
        permissions = (('can_view_likes', _('Can view likes')),)
