
from django.core.validators import MinValueValidator, MinLengthValidator
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField

from mylabour.models import TimeStampedModel, OpinionUserModel
from mylabour.utils import CHOICES_LEXERS

# отзывы о cource


class Course(TimeStampedModel):
    """

    """

    name = models.CharField(
        _('Name of cource'),
        max_length=200,
        unique=True,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)],
    )
    slug = AutoSlugField(_('Slug'), populate_from='name', always_update=True, unique=True, allow_unicode=True, db_index=True)
    picture = models.URLField(_('Picture'))
    decription = models.TextField(_('Description'))
    lexer = models.CharField(_('Lexer'), max_length=30, choices=CHOICES_LEXERS)
    authorship = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Authorship'),
        limit_choices_to={'is_superuser': True},
        related_name='cources',
    )

    class Meta:
        db_table = 'cources'
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        get_latest_by = 'date_added'
        ordering = ['name']

    objects = models.Manager()

    def __str__(self):
        return '{0.name}'.format(self)

    def save(self, *args, **kwargs):
        super(Course, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('app_cources:cource', kwargs={'slug': self.slug})


class Lesson(TimeStampedModel):
    """

    """

    name = models.CharField(
        _('Name'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(
        _('Slug'),
        populate_from='name',
        always_update=True,
        unique_with=['cource', 'name'],
        allow_unicode=True,
        db_index=True,
    )
    cource = models.ForeignKey('Course', verbose_name=_('Course'), on_delete=models.CASCADE, related_name='lessons')
    number = models.PositiveSmallIntegerField(_('Number of lesson'), validators=[MinValueValidator(1)])
    is_completed = models.BooleanField(_('Lesson is completed?'), default=False)
    header = models.TextField(_('Header'))
    conclusion = models.TextField(_('Conclusion'))
    views = models.IntegerField(_('Count views'), default=0, editable=False)
    opinions = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='opinions_about_lessons',
        through='OpinionAboutLesson',
        through_fields=['lesson', 'user'],
        verbose_name=_('Opinions'),
    )

    class Meta:
        db_table = 'Lessons'
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')
        get_latest_by = 'date_modified'
        ordering = ['cource', 'number']
        unique_together = ['name', 'cource', 'number']

    objects = models.Manager()

    def __str__(self):
        return '{0.name}'.format(self)

    def save(self, *args, **kwargs):
        super(Lesson, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('app_cources:lesson', kwargs={'number': self.number, 'slug': self.slug})


class Sublesson(TimeStampedModel):
    """

    """

    title = models.CharField(
        _('Title'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(
        _('Slug'),
        populate_from='title',
        unique_with=['lesson', 'title'],
        always_update=True,
        allow_unicode=True,
        db_index=True,
    )
    lesson = models.ForeignKey('Lesson', verbose_name=_('Lesson'), on_delete=models.CASCADE, related_name='sublessons')
    number = models.PositiveSmallIntegerField(_('Number of sublesson'), validators=[MinValueValidator(1)])
    text = models.TextField(_('Text'), help_text=_('Enter text what will be describe code.'))
    code = models.TextField(_('Code'), help_text=_('Enter code what will be dispayed by lexer.'))

    class Meta:
        db_table = 'sublessons'
        verbose_name = _('Sublesson')
        verbose_name_plural = _('Sublessons')
        get_latest_by = 'date_modified'
        ordering = ['number']
        unique_together = ['lesson', 'number']

    objects = models.Manager()

    def __str__(self):
        return '{0.title}'.format(self)


class OpinionAboutLesson(OpinionUserModel):
    """

    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        limit_choices_to={'is_active': True},
    )
    lesson = models.ForeignKey(
        'Lesson',
        verbose_name=_('Lesson'),
        on_delete=models.CASCADE,
        limit_choices_to={'is_completed': True},
    )

    class Meta(OpinionUserModel.Meta):
        db_table = 'opinions_about_lesson'
        verbose_name = _('Opinion about lesson')
        verbose_name_plural = _('Opinions about lesson')
        unique_together = ['user', 'lesson']
        ordering = ['lesson', 'user']

    objects = models.Manager()

    def __str__(self):
        return 'Opinion os user {0.user} about lesson "{0.lesson}"'.format(self)


class LessonComment(TimeStampedModel):
    """

    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'is_active': True},
        on_delete=models.DO_NOTHING,
        related_name='comments_lessons',
        verbose_name=_('Author'),
    )
    lesson = models.ForeignKey(
        'Lesson',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Lesson'),
    )
    content = models.TextField(_('Content'))

    class Meta:
        db_table = 'lessons_comments'
        verbose_name = _('Comment of lesson')
        verbose_name_plural = _('Comments of lesson')
        get_latest_by = 'date_modified'
        ordering = ['lesson', 'author']

    objects = models.Manager()

    def __str__(self):
        return 'Comment from user "{0.user}" on lesson "{0.lesson}"'.format(self)
