
from django.utils import timezone
from django.core.validators import MaxLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.models import GenericRelatable, Timestampable, UUIDable

from .constants import MAX_LENGTH_COMMENT

# comment design from website


class Comment(GenericRelatable, Timestampable, UUIDable):
    """ """

    text_comment = models.TextField(
        _('text comment'),
        validators=[
            MaxLengthValidator(
                MAX_LENGTH_COMMENT,
                _('Comment must be contains no more than {0} characters.').format(MAX_LENGTH_COMMENT)
            )
        ]
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('user'),
        on_delete=models.CASCADE, related_name='comments',
    )

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        get_latest_by = 'created'
        ordering = ('created', )

    def __str__(self):
        return _('{0.text_comment}').format(self)

    def is_new(self):
        """ """

        return self.created > timezone.now() - timezone.timedelta(days=settings.COUNT_DAYS_FOR_NEW_ELEMENTS)
    is_new.admin_order_field = 'created'
    is_new.short_description = _('Is new?')
    is_new.boolean = True
