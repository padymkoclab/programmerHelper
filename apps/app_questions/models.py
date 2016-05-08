
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinLengthValidator
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField

from apps.app_generic_models.models import UserComment_Generic, UserOpinion_Generic, UserLike_Generic
from apps.app_tags.models import Tag
from mylabour.models import TimeStampedModel

from .managers import QuestionManager


class Question(TimeStampedModel):
    """

    """

    OPEN_QUESTION = 'open'
    CLOSED_QUESTION = 'closed'

    CHOICES_STATUS = (
        (OPEN_QUESTION, _('Open question')),
        (CLOSED_QUESTION, _('Closed question')),
    )

    title = models.CharField(
        _('Title'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(_('Slug'), populate_from='title', unique=True, always_update=True, allow_unicode=True)
    text_question = models.TextField(_('Text question'))
    status = models.CharField(_('Status'), max_length=50, choices=CHOICES_STATUS, default=OPEN_QUESTION)
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
    opinions = GenericRelation(UserOpinion_Generic)

    objects = models.Manager()
    aaa = QuestionManager()

    class Meta:
        db_table = 'questions'
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['title']
        get_latest_by = 'date_added'

    def __str__(self):
        return _('Question "{0.title}"').format(self)

    def get_absolute_url(self):
        return reverse('app_questions:question', kwargs={'slug': self.slug})

    def has_acceptable_answer(self):
        return any(self.answers.values_list('is_acceptable', flat=True))

    # def count_good_opinions(self):
    #     return OpinionAboutQuestion.objects.filter(question=self, is_useful=True).count()

    # def count_bad_opinions(self):
    #     return OpinionAboutQuestion.objects.filter(question=self, is_useful=False).count()

    # def count_favorites(self):
    #     return OpinionAboutQuestion.objects.filter(question=self, is_favorite=OpinionUserModel.CHOICES_FAVORITE.yes).count()


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
        limit_choices_to={'status': Question.OPEN_QUESTION}
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        on_delete=models.DO_NOTHING,
        related_name='answers',
        limit_choices_to={'is_active': True},
    )
    is_acceptable = models.BooleanField(_('Is acceptable answer?'), default=False)
    comments = GenericRelation(UserComment_Generic)
    likes = GenericRelation(UserLike_Generic)

    class Meta:
        db_table = 'answers'
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        ordering = ['question', 'author']
        get_latest_by = 'date_modified'

    def __str__(self):
        return _('Answer on question "{0.question}" from user "{0.author}"').format(self)


# dynamic rating by field "voted_users"
# acceptend this answer only author
# top question and top answer by week
# top snippet by week
# are you have unread inbox messages
