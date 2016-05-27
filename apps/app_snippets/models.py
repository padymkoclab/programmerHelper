
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField

from apps.app_generic_models.models import CommentGeneric, OpinionGeneric
from apps.app_visits.models import Visit
from apps.app_tags.models import Tag
from mylabour.models import TimeStampedModel
from mylabour.constants import CHOICES_LEXERS

from .managers import SnippetManager
from .querysets import SnippetQuerySet


class Snippet(TimeStampedModel):
    """

    """

    title = models.CharField(
        _('Title'), max_length=200, unique=True, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(_('Slug'), populate_from='title', always_update=True, unique=True, allow_unicode=True, db_index=True)
    lexer = models.CharField(_('Lexer of code'), max_length=50, choices=CHOICES_LEXERS)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        related_name='snippets',
        on_delete=models.CASCADE,
        limit_choices_to={'is_active': True},
    )
    description = models.TextField(_('Decription'))
    code = models.TextField(_('Code'))
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('Tags'),
        related_name='snippets',
    )
    opinions = GenericRelation(OpinionGeneric)
    comments = GenericRelation(CommentGeneric)

    # managers
    objects = models.Manager()
    objects = SnippetManager.from_queryset(SnippetQuerySet)()

    class Meta:
        db_table = 'snippets'
        verbose_name = _("Snippet")
        verbose_name_plural = _("Snippets")
        get_latest_by = 'date_added'
        ordering = ['date_added']

    def __str__(self):
        return '{0.title}'.format(self)

    def get_absolute_url(self):
        return reverse('app_snippets:snippet', kwargs={'slug': self.slug})

    def get_scope(self):
        return self.__class__.objects.snippets_with_scopes().get(pk=self.pk).scope
    get_scope.short_description = _('Scope')

    def get_count_views(self):
        return Visit.objects.get_count_visits_by_url(self.get_absolute_url)
