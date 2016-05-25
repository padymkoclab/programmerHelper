
import functools

from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator, MinLengthValidator
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField

from apps.app_generic_models.models import CommentGeneric, OpinionGeneric
from mylabour.models import TimeStampedModel
from mylabour.constants import CHOICES_LEXERS

from .managers import CourseManager, CourseQuerySet

# отзывы о course


class Course(TimeStampedModel):
    """

    """

    MIN_COUNT_LESSONS = 3
    MAX_COUNT_LESSONS = 12
    MAX_COUNT_AUTHORS = 5

    name = models.CharField(
        _('Name'),
        max_length=200,
        unique=True,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)],
    )
    slug = AutoSlugField(_('Slug'), populate_from='name', always_update=True, unique=True, allow_unicode=True, db_index=True)
    picture = models.URLField(_('Picture'))
    description = models.TextField(_('Description'))
    lexer = models.CharField(_('Lexer'), max_length=30, choices=CHOICES_LEXERS)
    authorship = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Authorship'),
        limit_choices_to={'is_active': True},
        related_name='courses',
    )

    class Meta:
        db_table = 'courses'
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        get_latest_by = 'date_added'
        ordering = ['name']

    objects = models.Manager()
    objects = CourseManager.from_queryset(CourseQuerySet)()

    def __str__(self):
        return '{0.name}'.format(self)

    def save(self, *args, **kwargs):
        super(Course, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('app_courses:course_detail', kwargs={'slug': self.slug})

    def get_total_scope(self):
        return functools.reduce(lambda a, b: a + b, (lesson.get_scope() for lesson in self.lessons.iterator()))
    get_total_scope.short_description = _('Scope')

    def authorship_inline(self):
        return ', '.join(i.__str__() for i in self.authorship.iterator())


class Lesson(TimeStampedModel):
    """

    """

    MIN_COUNT_SUBLESSONS = 5
    MAX_COUNT_SUBLESSONS = 12

    name = models.CharField(
        _('Name'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(
        _('Slug'),
        populate_from='name',
        always_update=True,
        unique_with=['course', 'number'],
        allow_unicode=True,
        db_index=True,
    )
    course = models.ForeignKey('Course', verbose_name=_('Course'), on_delete=models.CASCADE, related_name='lessons')
    number = models.PositiveSmallIntegerField(_('Number of lesson'), validators=[MinValueValidator(1)])
    is_completed = models.BooleanField(_('Lesson is completed?'), default=False)
    header = models.TextField(_('Header'))
    conclusion = models.TextField(_('Conclusion'))
    views = models.IntegerField(_('Count views'), default=0, editable=False)
    comments = GenericRelation(CommentGeneric)
    opinions = GenericRelation(OpinionGeneric)

    class Meta:
        db_table = 'Lessons'
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')
        get_latest_by = 'date_modified'
        ordering = ['course', 'number']
        unique_together = ['course', 'number']

    objects = models.Manager()

    def __str__(self):
        return '{0.name}'.format(self)

    def save(self, *args, **kwargs):
        super(Lesson, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('app_courses:lesson_detail', kwargs={'number': self.number, 'slug': self.slug})

    def get_scope(self):
        count_good_opinions = self.opinions.filter(is_useful=True).count()
        count_bad_opinions = self.opinions.filter(is_useful=False).count()
        return count_good_opinions - count_bad_opinions
    get_scope.short_description = _('Scope')


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
        ordering = ['lesson', 'number']
        unique_together = ['lesson', 'number']

    objects = models.Manager()

    def __str__(self):
        return '{0.title}'.format(self)
