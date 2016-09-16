
import statistics

from django.utils import timezone
# from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinLengthValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.models import BaseGenericModel
from utils.django.validators import OnlyLettersValidator

from .querysets import ReplyQuerySet


class Reply(BaseGenericModel):
    """
    Model for reply about other objects.
    """

    MAX_MARK = 5
    MIN_MARK = 1

    ERROR_MSG_UNIQUE_USER_AND_OBJECT = _('Distinct user may has alone reply')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name=_('user'),
    )
    text_reply = models.CharField(
        _('text of reply'),
        validators=[MinLengthValidator(100)],
        max_length=1000,
        help_text=_('From 10 to 100 words.'),
    )
    advantages = ArrayField(
        models.CharField(max_length=20, validators=[OnlyLettersValidator]),
        size=10,
        verbose_name=_('advantages'),
        help_text=_('Listing from 1 to 10 words separated commas.'),
        error_messages={
            'blank': 'Enter at least one word.',
            'item_invalid': 'Word is not correct.',
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
    mark_for_content = models.PositiveSmallIntegerField(
        _('mark for content'),
        default=MIN_MARK,
        validators=[
            MaxValueValidator(
                MAX_MARK, _('The mark for content must be from 1 to {}'.format(MAX_MARK))
            )
        ])
    mark_for_style = models.PositiveSmallIntegerField(
        _('mark for style'),
        default=MIN_MARK,
        validators=[
            MaxValueValidator(
                MAX_MARK, _('The mark for style must be from 1 to {}'.format(MAX_MARK))
            )
        ])
    mark_for_language = models.PositiveSmallIntegerField(
        _('mark for language'),
        default=MIN_MARK,
        validators=[
            MaxValueValidator(
                MAX_MARK, _('The mark for language must be from 1 to {}'.format(MAX_MARK))
            )
        ])

    # managers
    objects = models.Manager()
    objects = ReplyQuerySet.as_manager()

    class Meta:
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

        super(Reply, self).save(*args, **kwargs)

    def is_new(self):
        return self.date_added > timezone.now() - timezone.timedelta(days=settings.COUNT_DAYS_FOR_NEW_ELEMENTS)
    is_new.admin_order_field = 'date_added'
    is_new.short_description = _('Is new?')
    is_new.boolean = True

    def get_total_mark(self):
        """ """

        if hasattr(self, 'total_mark'):
            return self.total_mark

        total_mark = statistics.mean(
            [self.mark_for_content, self.mark_for_language, self.mark_for_style]
        )

        return round(total_mark, 3)
    get_total_mark.admin_order_field = 'total_mark'
    get_total_mark.short_description = _('Total mark')
