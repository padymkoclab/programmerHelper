
from datetime import timedelta
import uuid

from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from mylabour.models_fields import ConfiguredAutoSlugField
from mylabour.models import TimeStampedModel

from .managers import TestQuestionManager, SuitQuerySet


class Suit(TimeStampedModel):
    """
    Model for suit of questions in test
    """

    MIN_COUNT_QUESTIONS_FOR_COMPLETED_SUIT = 7
    MAX_COUNT_QUESTIONS_FOR_COMPLETED_SUIT = 21

    SIMPLE = 'simple'
    MIDDLE = 'middle'
    COMPLICATED = 'complicated'

    CHOICES_COMPLEXITY = (
        (SIMPLE, _('Simple')),
        (MIDDLE, _('Middle')),
        (COMPLICATED, _('Complicated')),
    )

    UNCOMPLETED = 'uncompleted'
    COMPLETED = 'completed'

    CHOICES_STATUS = (
        (UNCOMPLETED, 'Uncompleted'),
        (COMPLETED, 'Completed'),
    )

    name = models.CharField(
        _('Name'), max_length=200, unique=True,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = ConfiguredAutoSlugField(_('Slug'), populate_from='name', unique=True)
    status = models.CharField(_('Status'), max_length=20, choices=CHOICES_STATUS, default=UNCOMPLETED)
    description = models.CharField(
        ('Description'), max_length=500,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    image = models.ImageField(_('Image'), max_length=1000)
    duration = models.DurationField(
        _('Duration'), default=timedelta(minutes=1),
        validators=[
            MinValueValidator(timedelta(minutes=1)),
            MaxValueValidator(timedelta(minutes=15)),
        ]
    )
    complexity = models.CharField(_('Complexity'), max_length=30, choices=CHOICES_COMPLEXITY)
    passages = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_('Passages'),
        through='Passage', through_fields=['suit', 'user'],
    )

    objects = models.Manager()
    objects = SuitQuerySet.as_manager()

    class Meta:
        db_table = 'testing_suits'
        verbose_name = _("Testing suit")
        verbose_name_plural = _("Testing suits")
        ordering = ['date_added']
        get_latest_by = 'date_modified'

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('testing:suit', kwargs={'slug': self.slug})

    def get_admin_url(self):
        return reverse('admin:testing_suit_change', args=(self.pk, ))


class TestQuestion(TimeStampedModel):
    """

    """

    MIN_COUNT_VARIANTS_FOR_FULL_QUESTION = 3
    MAX_COUNT_VARIANTS_FOR_FULL_QUESTION = 8

    title = models.CharField(
        _('Title'), max_length=200,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = ConfiguredAutoSlugField(populate_from='title', unique_with=['title', 'suit'])
    suit = models.ForeignKey(
        'Suit', verbose_name=_('Suit'),
        related_name='questions', on_delete=models.CASCADE,
    )
    text_question = models.CharField(_('Text question'), max_length=300)

    class Meta:
        db_table = 'testing_questions'
        verbose_name = _("Testing question")
        verbose_name_plural = _("Testing questions")
        unique_together = ('title', 'suit')
        get_latest_by = 'date_modified'
        ordering = ['suit', 'title']

    objects = models.Manager()
    objects = TestQuestionManager()

    def __str__(self):
        return '{0.title}'.format(self)

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('title', 'suit'):
            return _('This suit already has question with this title')
        return super().unique_error_message(model_class, unique_check)

    def get_admin_url(self):
        pass

    def is_completed_question(self):
        """ """

        return self.MIN_COUNT_VARIANTS <= self.variants <= self.MAX_COUNT_VARIANTS


class Variant(models.Model):
    """

    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    text_variant = models.CharField(_('Text variant'), max_length=300)
    question = models.ForeignKey(
        'TestQuestion', verbose_name=_('Question'),
        related_name='variants', on_delete=models.CASCADE,
    )
    is_right_variant = models.BooleanField(_('Is right variant of answer?'), default=False)

    class Meta:
        db_table = 'testing_variants'
        verbose_name = _("Variant")
        verbose_name_plural = _("Variants")
        unique_together = ['question', 'text_variant']
        ordering = ['question']

    def __str__(self):
        return '{0.text_variant}'.format(self)

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('question', 'text_variant'):
            return _('This question already has variant with this text')
        return super().unique_error_message(model_class, unique_check)


class Passage(models.Model):

    MIN_MARK = 0
    MAX_MARK = 10

    PASSED = 'passed'
    ATTEMPT = 'attempt'

    CHOICES_STATUS = (
        (PASSED, _('Passed')),
        (ATTEMPT, _('Attempt')),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('User'),
        on_delete=models.CASCADE, related_name='passages',
    )
    suit = models.ForeignKey('Suit', verbose_name=_('Suit'), on_delete=models.CASCADE)
    status = models.CharField(_('Status'), max_length=10, choices=CHOICES_STATUS)
    mark = models.SmallIntegerField(
        _('Mark'),
        validators=[
            MinValueValidator(MIN_MARK),
            MaxValueValidator(MAX_MARK),
        ]
    )
    date_passage = models.DateTimeField(_('Date passage'), auto_now_add=True)

    class Meta:
        db_table = 'testing_passages'
        verbose_name = _("Passage")
        verbose_name_plural = _("Passages")
        get_latest_by = 'date_passage'
        ordering = ['date_passage']

    def __str__(self):
        return 'Passage of user {self.user} on suit {0.suit} on {self.date_passage}'.format(self)
