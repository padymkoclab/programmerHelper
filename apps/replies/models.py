
from django.utils import timezone
# from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinLengthValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from mylabour.models import BaseGenericModel
from mylabour.validators import MaxCountWordsValidator, MinCountWordsValidator, OnlyLettersValidator

from .querysets import ReplyQuerySet


class Reply(BaseGenericModel):
    """
    Model for reply about other objects.
    """

    MAX_SCOPE = 5
    MIN_SCOPE = 1

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name=_('user'),
    )
    impress = models.CharField(
        _('impress (brief)'),
        max_length=50,
        validators=[MinLengthValidator(10)],
        help_text=_('From 10 to 50 characters.'),
    )
    advantages = ArrayField(
        models.CharField(max_length=20, validators=[OnlyLettersValidator]),
        size=10,
        verbose_name=_('advantages'),
        help_text=_('Listing from 1 to 10 words separated commas.'),
        error_messages={
            'blank': 'Enter at least one word.',
            # 'item_invalid': 'Word is not correct.',
        }
    )
    disadvantages = ArrayField(
        models.CharField(max_length=20, validators=[OnlyLettersValidator]),
        help_text=_('Listing from 1 to 10 words separated commas.'),
        verbose_name=_('disadvantages'),
        size=10,
        error_messages={
            'blank': 'Enter at least one word.',
            'item_invalid': 'Word is not correct.',
        }
    )
    text_reply = models.TextField(
        _('text of reply'),
        validators=[MinCountWordsValidator(10), MaxCountWordsValidator(100)],
        help_text=_('From 10 to 100 words.'),
    )
    scope_for_content = models.PositiveSmallIntegerField(
        _('scope for content'),
        default=MIN_SCOPE,
        validators=[
            MaxValueValidator(MAX_SCOPE, _('The scope for content must be from 1 to %d' % MAX_SCOPE))
        ])
    scope_for_style = models.PositiveSmallIntegerField(
        _('scope for style'),
        default=MIN_SCOPE,
        validators=[
            MaxValueValidator(MAX_SCOPE, _('The scope for style must be from 1 to %d' % MAX_SCOPE))
        ])
    scope_for_language = models.PositiveSmallIntegerField(
        _('scope for language'),
        default=MIN_SCOPE,
        validators=[
            MaxValueValidator(MAX_SCOPE, _('The scope for language must be from 1 to %d' % MAX_SCOPE))
        ])
    date_added = models.DateTimeField(_('Date aded'), auto_now_add=True)

    # managers
    objects = models.Manager()
    objects = ReplyQuerySet.as_manager()

    class Meta:
        db_table = 'replies'
        verbose_name = _('Reply')
        verbose_name_plural = _('Replies')
        get_latest_by = 'date_added'
        ordering = ['date_added']
        unique_together = ['user', 'object_id']

    def __str__(self):
        type_instance = self.content_object._meta.verbose_name.lower()
        return _('Reply on {0} "{1.content_object}" from {1.user}').format(type_instance, self)

    def save(self, *args, **kwargs):
        # each word must saved as capitalize
        self.disadvantages = tuple(word.capitalize() for word in self.disadvantages)
        self.advantages = tuple(word.capitalize() for word in self.advantages)
        # call save
        super(Reply, self).save(*args, **kwargs)

    def is_new(self):
        return self.date_added > timezone.now() - timezone.timedelta(days=settings.COUNT_DAYS_DISTINGUISH_ELEMENTS_AS_NEW)
    is_new.admin_order_field = 'date_added'
    is_new.short_description = _('Is new?')
    is_new.boolean = True

    def get_total_scope(self):
        return self.__class__.objects.replies_with_total_scope().get(pk=self.pk).total_scope
    get_total_scope.admin_order_field = 'total_scope'
    get_total_scope.short_description = _('Total scope')
