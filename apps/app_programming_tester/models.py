
from datetime import timedelta
import uuid

from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from autoslug import AutoSlugField
from model_utils import Choices

from mylabour.models import TimeStampedModel


class TestSuit(TimeStampedModel):
    """
    Model for suit of questions in test
    """

    CHOICES_COMPLEXITY = Choices(
        ('simple', _('Simple')),
        ('middle', _('Middle')),
        ('complicated', _('Complicated')),
        ('from_users', _('From users')),
    )

    name = models.CharField(
        _('Name'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(_('Slug'), populate_from='name', unique=True, always_update=True, allow_unicode=True, db_index=True)
    description = models.TextField(_('Description'))
    picture = models.URLField(_('Picture'), max_length=1000)
    duration = models.DurationField(_('Duration'), default=timedelta(minutes=1))
    count_attempts_passing = models.IntegerField(_('Count attemp passing'), default=0, editable=False)
    count_completed_passing = models.IntegerField(_('Count completed passing'), default=0, editable=False)
    complexity = models.CharField(_('Complexity'), max_length=50, choices=CHOICES_COMPLEXITY)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        on_delete=models.PROTECT,
        related_name='test_suits',
    )

    class Meta:
        db_table = 'test_suits'
        verbose_name = _("Suit of tests")
        verbose_name_plural = _("Suits of tests")
        ordering = ['date_added']
        get_latest_by = 'date_modified'
        unique_together = ['author', 'name']

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('app_programming_tester:test_suit', kwargs={'slug': self.slug})


class TestQuestion(TimeStampedModel):
    """

    """

    name = models.CharField(
        _('Name'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    test_suit = models.ForeignKey('TestSuit', verbose_name=_('Test suit'), related_name='questions', on_delete=models.CASCADE)
    text_question = models.TextField(_('Text question'))

    class Meta:
        db_table = 'test_suits_questions'
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


class Variant(models.Model):
    """

    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    question = models.ForeignKey('TestQuestion', related_name='variants', verbose_name=_('Question'), on_delete=models.CASCADE)
    text_variant = models.CharField(_('Text variant'), max_length=300)
    is_right_variant = models.BooleanField(_('It is right variant of answer?'), default=False)

    class Meta:
        db_table = 'test_suits_questions_variants'
        verbose_name = _("Variant answer on question")
        verbose_name_plural = _("Variants answer on question")
        unique_together = ['question', 'text_variant']
        order_with_respect_to = 'question'

    def __str__(self):
        return '{0.text_variant}'.format(self)
