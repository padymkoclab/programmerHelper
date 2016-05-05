
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField

from apps.app_tags.models import Tag
from mylabour.models import TimeStampedModel, OpinionUserModel
from mylabour.utils import CHOICES_LEXERS


class Snippet(TimeStampedModel):
    """

    """

    title = models.CharField(
        _('Title'), max_length=200, unique=True, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(_('Slug'), populate_from='title', always_update=True, unique=True, allow_unicode=True)
    lexer = models.CharField(_('Lexer of code'), max_length=50, choices=CHOICES_LEXERS)
    description = models.TextField(_('Decription'))
    code = models.TextField(_('Code'))
    views = models.IntegerField(_('Count views'), default=0, editable=False)
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('Tags'),
        related_name='snippets',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        related_name='snippets',
        on_delete=models.DO_NOTHING,
        limit_choices_to={'is_active': True},
    )
    opinions = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Opinions'),
        related_name='opinions_about_snippets',
        through='OpinionAboutSnippet',
        through_fields=('snippet', 'user'),
    )

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
        pass


class OpinionAboutSnippet(OpinionUserModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='User',
        limit_choices_to={'is_active': True},
    )
    snippet = models.ForeignKey('Snippet', on_delete=models.CASCADE, verbose_name='Snippet')

    class Meta(OpinionUserModel.Meta):
        db_table = 'Opinions_about_snippets'
        verbose_name = _('Opinion about snippet')
        verbose_name_plural = _('Opinions about snippet')
        ordering = ['snippet', 'user']
        unique_together = ['user', 'snippet']

    def __str__(self):
        return _('Opinion of user "{0.user}" about snippet "{0.snippet}"').format(self)


class SnippetComment(TimeStampedModel):

    text_comment = models.TextField(_('Text comment'))
    snippet = models.ForeignKey('Snippet', related_name='comments', verbose_name=_('Snippet'), on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='comments_snippet',
        verbose_name=_('Author'),
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        db_table = 'snippets_comments'
        verbose_name = _("Comment of snippet")
        verbose_name_plural = _("Comments of snippet")
        get_latest_by = 'date_added'
        ordering = ['snippet', 'date_added']

    def __str__(self):
        return _('Comment from "{0.author}" on snippet "{0.snippet}"').format(self)
