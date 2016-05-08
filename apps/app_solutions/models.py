
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinLengthValidator
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField

from apps.app_generic_models.models import UserComment_Generic, UserOpinion_Generic
from apps.app_web_links.models import WebLink
from apps.app_tags.models import Tag
from mylabour.models import TimeStampedModel
from mylabour.utils import CHOICES_LEXERS


class SolutionCategory(TimeStampedModel):
    """

    """

    name = models.CharField(
        _('name'), max_length=200, unique=True, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
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

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('app_solutions:solution_category', kwargs={'slug': self.slug})

    # latest changed


class Solution(TimeStampedModel):
    """

    """

    title = models.CharField(
        _('Title'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(_('Slug'), populate_from='title', unique_with=['category'], always_update=True, allow_unicode=True)
    body = models.TextField(_('Text solution'))
    category = models.ForeignKey(
        'SolutionCategory',
        on_delete=models.CASCADE,
        related_name='solutions',
        verbose_name=_('Category'),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='solutions',
        verbose_name=_('Author'),
        on_delete=models.DO_NOTHING,
    )
    views = models.IntegerField(_('Count views'), default=0, editable=False)
    tags = models.ManyToManyField(
        Tag,
        related_name='solutions',
        verbose_name=_('Tags'),
    )
    useful_links = models.ManyToManyField(
        WebLink,
        related_name='solutions',
        verbose_name=_('Useful links'),
    )
    comments = GenericRelation(UserComment_Generic)
    opinions = GenericRelation(UserOpinion_Generic)

    # run code JSBin
    # testing with online run code

    class Meta:
        db_table = 'solutions'
        verbose_name = _("Solution")
        verbose_name_plural = _("Solutions")
        ordering = ['category', 'title']
        unique_together = ['title', 'category']
        get_latest_by = 'date_added'

    def __str__(self):
        return _('Solution "{0.title}"').format(self)

    def get_absolute_url(self):
        return reverse('app_solutions:solution', kwargs={'slug': self.slug})

    # def count_votes_as_good_solution(self):
    #     return self.voted_users.through.objects.filter(solution=self, is_helped=True).count()

    # def count_votes_as_bad_solution(self):
    #     return self.voted_users.through.objects.filter(solution=self, is_helped=False).count()

    # def all_count_votes(self):
    #     return self.count_votes_as_good_solution() + self.count_votes_as_bad_solution()

    def get_scope_solution(self):
        pass
