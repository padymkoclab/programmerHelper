
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinLengthValidator
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField

from apps.comments.models import Comment
from apps.opinions.models import Opinion
from apps.web_links.models import WebLink
from apps.tags.models import Tag
from mylabour.models import TimeStampedModel
from mylabour.constants import CHOICES_LEXERS

from .managers import SolutionQuerySet, SolutionCategoryManager


class SolutionCategory(TimeStampedModel):
    """

    """

    name = models.CharField(
        _('name'), max_length=100, unique=True, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(_('Slug'), populate_from='name', unique=True, always_update=True, allow_unicode=True)
    description = models.TextField(_('Description'))
    lexer = models.CharField(_('Lexer of code'), max_length=100, choices=CHOICES_LEXERS)

    class Meta:
        db_table = 'solutions_categories'
        verbose_name = _("Category of solutions")
        verbose_name_plural = _("Categories of solutions")
        get_latest_by = 'date_modified'
        ordering = ['lexer', 'name']

    objects = models.Manager()
    objects = SolutionCategoryManager()

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('solutions:category', kwargs={'slug': self.slug})

    def get_total_scope(self):
        return sum(solution.get_scope() for solution in self.solutions.iterator())
    get_total_scope.short_description = _('Scope')

    def last_activity(self):
        return self.solutions.latest().date_modified
    last_activity.short_description = _('Last activity')


class Solution(TimeStampedModel):
    """

    """

    title = models.CharField(
        _('Title'), max_length=100, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(_('Slug'), populate_from='title', unique_with=['category'], always_update=True, allow_unicode=True)
    body = models.TextField(_('Text solution'))
    category = models.ForeignKey(
        'SolutionCategory',
        on_delete=models.CASCADE,
        related_name='solutions',
        verbose_name=_('Category'),
    )
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='solutions',
        verbose_name=_('Author'),
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='solutions',
        verbose_name=_('Tags'),
    )
    links = models.ManyToManyField(
        WebLink,
        related_name='solutions',
        verbose_name=_('Useful links'),
    )
    comments = GenericRelation(Comment)
    opinions = GenericRelation(Opinion)

    # managers
    objects = models.Manager()
    # objects = SolutionManager.from_queryset(SolutionQuerySet)()

    class Meta:
        db_table = 'solutions'
        verbose_name = _("Solution")
        verbose_name_plural = _("Solutions")
        ordering = ['category', 'title']
        unique_together = ['title', 'category']
        get_latest_by = 'date_modified'

    def __str__(self):
        return _('{0.title}').format(self)

    def get_absolute_url(self):
        return reverse('solutions:solution', kwargs={'slug': self.slug})

    def get_scope(self):
        count_good_opinions = self.opinions.filter(is_useful=True).count()
        count_bad_opinions = self.opinions.filter(is_useful=False).count()
        return count_good_opinions - count_bad_opinions
    get_scope.short_description = _('Scope')