
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.models import GenericRelatable, Timestampable, UUIDable, OverrrideUniqueTogetherErrorMessages

from .managers import OpinionManager
from .querysets import OpinionQuerySet


class Opinion(OverrrideUniqueTogetherErrorMessages, GenericRelatable, Timestampable, UUIDable):

    UNIQUE_TOGETHER_ERROR_MESSAGES = _('User already has opinion about this object')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='opinions',
        verbose_name=_('user'),
    )
    is_useful = models.BooleanField(_('is useful?'))

    objects = models.Manager()
    objects = OpinionManager.from_queryset(OpinionQuerySet)()

    class Meta:
        verbose_name = _('opinion')
        verbose_name_plural = _('opinions')
        get_latest_by = 'updated'
        ordering = ('updated', )
        # permissions = (('can_view_opinions', _('Can view opinions')),)
        unique_together = (('user', 'object_id'))

    def __str__(self):
        return _('About {0} "{1}"').format(
            self.content_type.model_class()._meta.verbose_name.lower(),
            self.content_object.__str__(),
        )

    def save(self, *args, **kwargs):
        super(Opinion, self).save(*args, **kwargs)

    def clean(self):

        if self.content_object and hasattr(self.content_object, 'user'):
            if self.content_object.user == self.user:
                raise ValidationError(_('Author not allowed have opinion about hisself labour.'))
