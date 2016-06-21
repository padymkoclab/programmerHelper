
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from mylabour.fields_db import ConfiguredAutoSlugField
from apps.comments.models import Comment
from apps.opinions.models import Opinion
from apps.favours.models import Favour
from apps.visits.models import Visit
from apps.tags.models import Tag
from mylabour.models import TimeStampedModel
from mylabour.constants import CHOICES_LEXERS

from .managers import SnippetManager
from .querysets import SnippetQuerySet


class Snippet(TimeStampedModel):
    """
    Model for snippet.
    """

    CHOICES_LEXERS = CHOICES_LEXERS

    title = models.CharField(
        _('Title'), max_length=200, unique=True, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = ConfiguredAutoSlugField(_('Slug'), populate_from='title', unique=True)
    lexer = models.CharField(_('Lexer of code'), max_length=50, choices=CHOICES_LEXERS)
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        related_name='snippets',
        on_delete=models.CASCADE,
        limit_choices_to={'is_active': True},
    )
    description = models.TextField(_('Decription'), validators=[MinLengthValidator(15)])
    code = models.TextField(_('Code'), validators=[MinLengthValidator(5)])
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('Tags'),
        related_name='snippets',
    )
    opinions = GenericRelation(Opinion, related_query_name='snippets')
    comments = GenericRelation(Comment, related_query_name='snippets')
    favours = GenericRelation(Favour, related_query_name='snippets')

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

    def save(self, *args, **kwargs):
        super(Snippet, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('snippets:detail', kwargs={'slug': self.slug})

    def get_scope(self):
        return self.__class__.objects.snippets_with_scopes().get(pk=self.pk).scope
    get_scope.admin_order_field = 'scope'
    get_scope.short_description = _('Scope')

    def get_count_views(self):
        return Visit.objects.get_count_visits_by_url(self.get_absolute_url)

    def show_users_given_bad_opinions(self):
        """Return the users determined this snippet as not useful."""

        return self.opinions.filter(is_useful=False).values_list('account__username', flat=True)

    def show_users_given_good_opinions(self):
        """Return the users determined this snippet as useful."""

        return self.opinions.filter(is_useful=True).values_list('account__username', flat=True)

    def related_snippets(self):
        """ """
        raise NotImplementedError
        # analysis tags
        # analysis title
