
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinLengthValidator
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField
from model_utils import Choices
from model_utils.managers import QueryManager

from apps.app_generic_models.models import CommentGeneric, OpinionGeneric, LikeGeneric
from apps.app_tags.models import Tag
from mylabour.models import TimeStampedModel

from .managers import QuestionManager, AnswerManager


class Question(TimeStampedModel):
    """

    """

    CHOICES_STATUS = Choices(
        ('open', _('Open')),
        ('closed', _('Closed')),
    )

    title = models.CharField(
        _('Title'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(_('Slug'), populate_from='title', unique=True, always_update=True, allow_unicode=True)
    text_question = models.TextField(_('Text question'))
    status = models.CharField(_('Status'), max_length=50, choices=CHOICES_STATUS, default=CHOICES_STATUS.open)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        related_name='questions',
        on_delete=models.DO_NOTHING,
        limit_choices_to={'is_active': True},
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='questions',
        verbose_name=_('Tags'),
    )
    views = models.IntegerField(_('Count views'), default=0, editable=False)
    is_dublicated = models.BooleanField(_('Is dublicated question?'), default=False)
    opinions = GenericRelation(OpinionGeneric)

    # managers
    objects = models.Manager()
    objects = QuestionManager()

    # simple managers
    open_questions = QueryManager(status=CHOICES_STATUS.open)
    closed_questions = QueryManager(status=CHOICES_STATUS.closed)
    questions_with_acceptabled_answer = QueryManager(answers__is_acceptabled=True)

    class Meta:
        db_table = 'questions'
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['title']
        get_latest_by = 'date_added'

    def __str__(self):
        return _('{0.title}').format(self)

    def get_absolute_url(self):
        return reverse('app_questions:question', kwargs={'slug': self.slug})

    def has_acceptabled_answer(self):
        count_acceptabled_answers = self.answers.filter(is_acceptabled=True).count()
        if count_acceptabled_answers == 0:
            return False
        elif count_acceptabled_answers == 1:
            return True
        else:
            error_message = ugettext('Question "{0}" have more than a single acceptabled answer!'.format(self.title))
            raise ValidationError(error_message)
    has_acceptabled_answer.boolean = True

    def get_scope(self):
        good_opinions = self.opinions.filter(is_useful=True).count()
        bad_opinions = self.opinions.filter(is_useful=False).count()
        return good_opinions - bad_opinions
    get_scope.short_description = _('Scope')

    def last_activity(self):
        return self.answers.latest().date_modified
    last_activity.short_description = _('Last activity')

    def get_count_favorites(self):
        return self.opinions.filter(is_favorite=True).count()
    get_count_favorites.short_description = _('Count favorites')

    def get_count_unfavorites(self):
        return self.opinions.filter(is_favorite=False).count()
    get_count_unfavorites.short_description = _('Count unfavorites')


class Answer(TimeStampedModel):
    """

    """

    text_answer = models.TextField(
        _('Text of answer'), validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    question = models.ForeignKey(
        'Question',
        verbose_name=_('Question'),
        on_delete=models.CASCADE,
        related_name='answers',
        limit_choices_to={'status': Question.CHOICES_STATUS.open}
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        on_delete=models.DO_NOTHING,
        related_name='answers',
        limit_choices_to={'is_active': True},
    )
    is_acceptabled = models.BooleanField(_('Is acceptabled answer?'), default=False)
    comments = GenericRelation(CommentGeneric)
    likes = GenericRelation(LikeGeneric)

    objects = models.Manager()
    objects = AnswerManager()

    # simple managers
    acceptabled_answers = QueryManager(is_acceptabled=True)

    class Meta:
        db_table = 'answers'
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        ordering = ['question', 'author']
        get_latest_by = 'date_modified'

    def __str__(self):
        return _('Answer on question "{0.question}" from user "{0.author}"').format(self)

    def get_scope(self):
        count_likes = self.likes.filter(liked_it=True).count()
        count_dislikes = self.likes.filter(liked_it=False).count()
        return count_likes - count_dislikes
    get_scope.short_description = _('Scope')
