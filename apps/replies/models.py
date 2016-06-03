
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from mylabour.models import BaseGenericModel
from mylabour.validators import MaxCountWordsValidator


class Reply(BaseGenericModel):

    MAX_SCOPE = 5

    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name=_('User'),
    )
    impress = models.CharField(_('Impress (brief).'), max_length=50, validators=[MinLengthValidator(10)])
    advantages = models.CharField(
        _('Andvantages'),
        max_length=100,
        validators=[MaxCountWordsValidator(10)],
        help_text=_('Maximum 10 words.')
    )
    disadvantages = models.CharField(
        _('Disandvantages'),
        max_length=100,
        validators=[MaxCountWordsValidator(10)],
        help_text=_('Maximum 10 words.')
    )
    text_reply = models.TextField(
        _('Text of reply'),
        validators=[MinLengthValidator(20), MaxCountWordsValidator(100)],
        help_text=_('Maximum 100 words.'),
    )
    scope_for_content = models.PositiveSmallIntegerField(
        _('Scope for content'),
        default=0,
        validators=[
            MaxValueValidator(MAX_SCOPE, _('Scope for content must from 0 to %d' % MAX_SCOPE))
        ])
    scope_for_style = models.PositiveSmallIntegerField(
        _('Scope for style'),
        default=0,
        validators=[
            MaxValueValidator(MAX_SCOPE, _('Scope for style must from 0 to %d' % MAX_SCOPE))
        ])
    scope_for_language = models.PositiveSmallIntegerField(
        _('Scope for language'),
        default=0,
        validators=[
            MaxValueValidator(MAX_SCOPE, _('Scope for language must from 0 to %d' % MAX_SCOPE))
        ])
    date_added = models.DateTimeField(_('Date aded'), auto_now_add=True)

    class Meta:
        db_table = 'replies'
        verbose_name = _('Reply')
        verbose_name_plural = _('Replies')
        get_latest_by = 'date_added'
        ordering = ['date_added']
        unique_together = ['account', 'object_id']

    def __str__(self):
        type_instance = self.content_object._meta.verbose_name.lower()
        return _('Reply on {0} "{1.content_object}" from {1.account}').format(type_instance, self)

    def is_new(self):
        return self.date_added > timezone.now() - timezone.timedelta(days=settings.COUNT_DAYS_DISTINGUISH_ELEMENTS_AS_NEW)
    is_new.admin_order_field = 'date_added'
    is_new.short_description = _('Is new?')
    is_new.boolean = True

    def get_total_scope(self):
        raise Exception('')
