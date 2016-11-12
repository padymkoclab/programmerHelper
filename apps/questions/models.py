
import logging

from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinLengthValidator
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.models import Timestampable, UUIDable
from utils.django.models_fields import ConfiguredAutoSlugField
from utils.django.models_utils import get_admin_url

from apps.comments.models import Comment
from apps.comments.managers import CommentManager
from apps.comments.modelmixins import CommentModelMixin
from apps.opinions.models import Opinion
from apps.opinions.managers import OpinionManager
from apps.opinions.modelmixins import OpinionModelMixin
from apps.tags.models import Tag
from apps.tags.managers import TagManager
from apps.tags.modelmixins import TagModelMixin

from .managers import QuestionManager, AnswerManager
from .querysets import QuestionQuerySet, AnswerQuerySet


logger = logging.getLogger('django.development')

logger.warning('scrapy data question from StackOverFlow or MailList Google Groups by tags Django, JS as latest')


class Question(TagModelMixin, OpinionModelMixin, Timestampable, UUIDable):
    """

    """

    OPEN = 'OPEN'
    CLOSED = 'CLOSED'

    CHOICES_STATUS = (
        ('OPEN', _('Open')),
        ('CLOSED', _('Closed')),
    )

    title = models.CharField(
        _('Title'), max_length=200,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = ConfiguredAutoSlugField(populate_from='title', unique=True)
    text_question = models.TextField(_('Text question'))
    status = models.CharField(_('Status'), max_length=50, choices=CHOICES_STATUS, default=OPEN)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('User'),
        related_name='questions', on_delete=models.CASCADE,
    )
    count_views = models.PositiveIntegerField(_('count views'), editable=False, default=0)
    tags = models.ManyToManyField(
        Tag, related_name='questions', verbose_name=_('Tags'),
    )
    opinions = GenericRelation(Opinion, related_query_name='questions')

    # managers
    objects = models.Manager()
    objects = QuestionManager.from_queryset(QuestionQuerySet)()

    opinions_manager = OpinionManager()
    tags_manager = TagManager()

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['-created']
        get_latest_by = 'created'

    def __str__(self):
        return _('{0.title}').format(self)

    def get_absolute_url(self):

        return reverse('questions:question', kwargs={'slug': self.slug})

    def get_admin_url(self):

        return get_admin_url(self)

    def get_count_answers(self):
        """ """

        if hasattr(self, 'count_answers'):
            return self.count_answers

        return self.answers.count()
    get_count_answers.admin_order_field = 'count_answers'
    get_count_answers.short_description = _('Count answers')

    def has_accepted_answer(self):
        """ """

        if hasattr(self, '_has_accepted_answer'):
            return self._has_accepted_answer

        if self.answers.filter(is_accepted=True).exists():
            return True
        return False
    has_accepted_answer.short_description = _('Has accepted answer?')
    has_accepted_answer.admin_order_field = '_has_accepted_answer'
    has_accepted_answer.boolean = True

    def get_date_latest_activity(self):
        """ """

        if hasattr(self, 'date_latest_activity'):
            return self.date_latest_activity

        if self.answers.exists():
            return self.answers.latest().updated
        return self.updated
    get_date_latest_activity.short_description = _('Date latest activity')
    get_date_latest_activity.admin_order_field = 'date_latest_activity'

    def related_questions(self):
        raise NotImplementedError
        # analysis tags


class Answer(OpinionModelMixin, CommentModelMixin, Timestampable, UUIDable):
    """

    """

    ERROR_MSG_UNIQUE_TOGETHER_USER_AND_QUESTION = _('This user already gave an answer on this question')

    text_answer = models.TextField(_('Text of answer'), validators=[MinLengthValidator(20)])
    question = models.ForeignKey(
        'Question', verbose_name=_('Question'),
        on_delete=models.CASCADE, related_name='answers',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('User'),
        on_delete=models.CASCADE, related_name='answers',
    )
    is_accepted = models.BooleanField(_('Is accepted answer?'), default=False)

    comments = GenericRelation(Comment, related_query_name='answers')
    opinions = GenericRelation(Opinion, related_query_name='answers')

    objects = models.Manager()
    objects = AnswerManager.from_queryset(AnswerQuerySet)()

    opinions_manager = OpinionManager()
    comments_manager = CommentManager()

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        ordering = ['question', 'user']
        get_latest_by = 'updated'
        unique_together = [('user', 'question')]

    def __str__(self):
        return _('{0.question}').format(self)

    def unique_error_message(self, model_class, unique_check):

        if model_class == type(self) and unique_check == ('user', 'question'):
            return self.ERROR_MSG_UNIQUE_TOGETHER_USER_AND_QUESTION
        return super().unique_error_message(model_class, unique_check)

    def time_after_published_question(self):
        return self.created - self.question.created
