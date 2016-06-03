
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from mylabour.models import BaseGenericModel
from mylabour.validators import MinCountWordsValidator


# comment design from website


class Comment(BaseGenericModel):

    MIN_LENGTH_COMMENT = 3

    text_comment = models.TextField(
        _('Text comment'),
        validators=[
            MinCountWordsValidator(
                MIN_LENGTH_COMMENT,
                _('Comment must be contains at least {0} words.').format(MIN_LENGTH_COMMENT)
            )
        ]
    )
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Author'),
    )
    rating = models.SmallIntegerField(_('Rating'), default=0, editable=False)
    date_modified = models.DateTimeField(_('Date last changed'), auto_now=True)
    date_added = models.DateTimeField(_('Date added'), auto_now_add=True)

    class Meta:
        db_table = 'comments'
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        get_latest_by = 'date_added'
        ordering = ['date_added']

    def __str__(self):
        return _('Comment on {0} "{1}"').format(
            self.content_object._meta.verbose_name.lower(),
            self.content_object.__str__()
        )

    def is_new(self):
        return self.date_added > timezone.now() - timezone.timedelta(days=settings.COUNT_DAYS_DISTINGUISH_ELEMENTS_AS_NEW)
    is_new.admin_order_field = 'date_added'
    is_new.short_description = _('Is new?')
    is_new.boolean = True
