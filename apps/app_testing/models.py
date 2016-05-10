
from datetime import timedelta
import uuid

from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from autoslug import AutoSlugField
from model_utils import Choices
from model_utils.fields import StatusField

from mylabour.models import TimeStampedModel


class TestingSuit(TimeStampedModel):
    """
    Model for suit of questions in test
    """

    MIN_COUNT_QUESTIONS = 12
    MAX_COUNT_QUESTIONS = 21

    CHOICES_COMPLEXITY = Choices(
        ('simple', _('Simple')),
        ('middle', _('Middle')),
        ('complicated', _('Complicated')),
        ('from_users', _('From users')),
    )

    name = models.CharField(
        _('Name'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(_('Slug'), populate_from='name', unique_with=['author'], always_update=True, allow_unicode=True, db_index=True)
    description = models.TextField(_('Description'))
    picture = models.URLField(_('Picture'), max_length=1000)
    duration = models.DurationField(_('Duration'), default=timedelta(minutes=1))
    complexity = models.CharField(_('Complexity'), max_length=50, choices=CHOICES_COMPLEXITY)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        on_delete=models.PROTECT,
        related_name='test_suits',
    )
    passages = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Passages'),
        related_name='passages',
        through='TestingPassage',
        through_fields=['test_suit', 'user'],
    )

    class Meta:
        db_table = 'testing_suits'
        verbose_name = _("Suit of tests")
        verbose_name_plural = _("Suits of tests")
        ordering = ['date_added']
        get_latest_by = 'date_modified'
        unique_together = ['author', 'name']

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('app_testing:suit', kwargs={'slug': self.slug})

    def count_attempts_passing(self):
        pass

    def count_completed_passing(self):
        pass


class TestingPassage(models.Model):

    MIN_SCOPE = 0
    MAX_SCOPE = 12

    CHOICES_STATUS = Choices(
        ('passed', _('Passed')),
        ('attemps', _('Attemps')),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    test_suit = models.ForeignKey(
        'TestingSuit',
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    status = StatusField(_('Status'), choices_name='CHOICES_STATUS')
    scope = models.SmallIntegerField(_('Scope'), default=0, editable=False)
    date_passage = models.DateTimeField(_('Date passage'), auto_now_add=True)

    class Meta:
        db_table = 'testing_passages'
        verbose_name = _("Testing passage")
        verbose_name_plural = _("Testing passages")
        get_latest_by = 'date_passage'
        order_with_respect_to = 'date_passage'


class TestingQuestion(TimeStampedModel):
    """

    """

    MIN_COUNT_VARIANTS = 3
    MAX_COUNT_VARIANTS = 8

    name = models.CharField(
        _('Name'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    test_suit = models.ForeignKey('TestingSuit', verbose_name=_('Test suit'), related_name='questions', on_delete=models.CASCADE)
    text_question = models.TextField(_('Text question'))

    class Meta:
        db_table = 'testing_questions'
        verbose_name = _("Testing question")
        verbose_name_plural = _("Testing questions")
        unique_together = ['name', 'test_suit']
        get_latest_by = 'date_modified'
        order_with_respect_to = 'test_suit'

    def __str__(self):
        return '{0.name}'.format(self)

    def have_one_right_variant(self):
        for variant in self.variants.all():
            if variant.is_right_variant:
                return True
        return False


class TestingVariant(models.Model):
    """

    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    question = models.ForeignKey('TestingQuestion', related_name='variants', verbose_name=_('Question'), on_delete=models.CASCADE)
    text_variant = models.CharField(_('Text variant'), max_length=300)
    is_right_variant = models.BooleanField(_('It is right variant of answer?'), default=False)

    class Meta:
        db_table = 'testing_variants'
        verbose_name = _("Variant")
        verbose_name_plural = _("Variants")
        unique_together = ['question', 'text_variant']
        order_with_respect_to = 'question'

    def __str__(self):
        return '{0.text_variant}'.format(self)
