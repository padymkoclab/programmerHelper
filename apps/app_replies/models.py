
from django.utils import timezone
from django.core.validators import MinLengthValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from mylabour.models import BaseGenericModel
from mylabour.validators import MaxCountWordsValidator


class Reply(BaseGenericModel):

    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name=_('User'),
    )
    impress = models.CharField(_('Impress (brief).'), max_length=50, validators=[MinLengthValidator(10)])
    advantages = models.CharField(
        _('Andvantages'),
        max_length=50,
        validators=[MaxCountWordsValidator(10)],
        help_text=_('Maximim 10 words.')
    )
    disandvantages = models.CharField(
        _('Disandvantages'),
        max_length=50,
        validators=[MaxCountWordsValidator(10)],
        help_text=_('Maximim 10 words.')
    )
    text_reply = models.TextField(
        _('Text of reply'),
        validators=[MinLengthValidator(20), MaxCountWordsValidator(100)],
        help_text=_('Maximum 100 words.'),
    )
    scope_for_content = models.PositiveSmallIntegerField(_('Scope for content'), default=0, validators=[MaxValueValidator(5)])
    scope_for_style = models.PositiveSmallIntegerField(_('Scope for style'), default=0, validators=[MaxValueValidator(5)])
    scope_for_language = models.PositiveSmallIntegerField(_('Scope for language'), default=0, validators=[MaxValueValidator(5)])
    date_added = models.DateTimeField(_('Date aded'), auto_now_add=True)

    class Meta:
        db_table = 'replies'
        verbose_name = _('Reply')
        verbose_name_plural = _('Replies')
        get_latest_by = 'date_added'
        ordering = ['date_added']

    def __str__(self):
        return ('Reply on {0.content_type} "{0.object_id}" from {0.account}').format(self)

    def clean(self):
        # restrict ability of user have only 3 replies on the object
        pass

    def is_new(self):
        return self.date_added > timezone.now() - timezone.timedelta(days=settings.COUNT_DAYS_DISTINGUISH_ELEMENTS_AS_NEW)
    is_new.admin_order_field = 'date_added'
    is_new.short_description = _('Is new?')
    is_new.boolean = True

    def get_total_scope(self):
        raise Exception('')
