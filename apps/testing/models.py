
from datetime import timedelta
import uuid

from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from utils.django.functions_db import Round
from utils.django.models_fields import ConfiguredAutoSlugField
from utils.django.models import TimeStampedModel
from utils.django.models_utils import get_admin_url

from .managers import SuitManager, QuestionManager, PassageManager
from .querysets import SuitQuerySet, QuestionQuerySet


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

    def upload_image(instance, filename):

        return '{}/{}/{}/{}'.format(
            instance._meta.app_label,
            instance._meta.model_name,
            instance.slug,
            filename,
        )

    name = models.CharField(
        _('Name'), max_length=200, unique=True,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = ConfiguredAutoSlugField(populate_from='name', unique=True)
    status = models.BooleanField(('Is completed'), default=False)
    description = models.CharField(
        ('Description'), max_length=500,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    image = models.ImageField(_('Image'), max_length=1000, upload_to=upload_image)
    duration = models.DurationField(
        _('Duration'), default=timedelta(minutes=1),
        validators=[
            MinValueValidator(timedelta(minutes=1)),
            MaxValueValidator(timedelta(minutes=15)),
        ]
    )
    complexity = models.CharField(_('Complexity'), max_length=30, choices=CHOICES_COMPLEXITY)
    testers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_('Testers'),
        through='Passage', through_fields=['suit', 'user'],
    )

    objects = models.Manager()
    objects = SuitManager.from_queryset(SuitQuerySet)()

    class Meta:
        verbose_name = _("Suit")
        verbose_name_plural = _("Suits")
        ordering = ['created']
        get_latest_by = 'updated'

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('testing:suit', kwargs={'slug': self.slug})

    def get_admin_url(self):
        return get_admin_url(self)

    def get_count_questions(self):
        """ """

        return self.questions.count()
    get_count_questions.short_description = _('Count questions')
    get_count_questions.admin_order_field = 'count_questions'

    def get_count_passages(self):
        """ """

        return self.passages.count()
    get_count_passages.short_description = _('Count passages')
    get_count_passages.admin_order_field = 'count_passages'

    def get_count_attempt_passages(self):
        """ """

        return self.passages.filter(status=self.testers.through.ATTEMPT).count()
    get_count_attempt_passages.short_description = _('Count attempt passages')

    def get_count_passed_passages(self):
        """ """

        return self.passages.filter(status=self.testers.through.PASSED).count()
    get_count_passed_passages.short_description = _('Count passed passages')

    def get_count_distinct_testers(self):
        """ """

        return self.testers.distinct().count()
    get_count_distinct_testers.short_description = _('Count distinct testers')

    def get_avg_mark(self):
        """ """

        return self.passages.aggregate(avg=Round(models.Avg('mark')))['avg']
    get_avg_mark.short_description = _('Average mark')


class Question(TimeStampedModel):
    """

    """

    MSG_UNIQUE_TOGETHER_TITLE_AND_SUIT = _('This suit already has a question with this title')

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
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        unique_together = ('title', 'suit')
        get_latest_by = 'updated'
        ordering = ['suit', 'title']

    objects = models.Manager()
    objects = QuestionManager.from_queryset(QuestionQuerySet)()

    def __str__(self):
        return '{0.title}'.format(self)

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('title', 'suit'):
            return self.MSG_UNIQUE_TOGETHER_TITLE_AND_SUIT
        return super().unique_error_message(model_class, unique_check)

    def get_admin_url(self):
        return get_admin_url(self)

    def is_completed(self):
        """ """

        return self.MIN_COUNT_VARIANTS_FOR_FULL_QUESTION <= self.variants.count() \
            <= self.MAX_COUNT_VARIANTS_FOR_FULL_QUESTION
    is_completed.short_description = _('Is completed?')
    is_completed.admin_order_field = 'status_completeness'
    is_completed.boolean = True

    def get_count_variants(self):
        """ """

        return self.variants.count()
    get_count_variants.short_description = _('Count variants')
    get_count_variants.admin_order_field = 'count_variants'


class Variant(models.Model):
    """

    """

    MSG_UNIQUE_TOGETHER_QUESTION_AND_TEXT_VARIANT = _('This question already has a variant with this text')

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    text_variant = models.CharField(_('Text variant'), max_length=300)
    question = models.ForeignKey(
        'Question', verbose_name=_('Question'),
        related_name='variants', on_delete=models.CASCADE,
    )
    is_right_variant = models.BooleanField(_('Is right variant of answer?'), default=False)

    class Meta:
        verbose_name = _("Variant")
        verbose_name_plural = _("Variants")
        unique_together = ['question', 'text_variant']
        ordering = ['question']

    def __str__(self):
        return '{0.text_variant}'.format(self)

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('question', 'text_variant'):
            return self.MSG_UNIQUE_TOGETHER_QUESTION_AND_TEXT_VARIANT
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
    suit = models.ForeignKey(
        'Suit', verbose_name=_('Suit'),
        on_delete=models.CASCADE, related_name='passages',
    )
    status = models.CharField(_('Status'), max_length=10, choices=CHOICES_STATUS)
    mark = models.SmallIntegerField(
        _('Mark'),
        validators=[
            MinValueValidator(MIN_MARK),
            MaxValueValidator(MAX_MARK),
        ]
    )
    created = models.DateTimeField(_('Created'), auto_now_add=True)

    objects = models.Manager()
    objects = PassageManager()

    class Meta:
        verbose_name = _("Passage")
        verbose_name_plural = _("Passages")
        get_latest_by = 'created'
        ordering = ['created']

    def __str__(self):
        return _('In suit "{0.suit}"').format(self)
