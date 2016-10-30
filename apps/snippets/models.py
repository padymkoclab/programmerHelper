
import collections

from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.models_utils import get_admin_url
from utils.django.models_fields import ConfiguredAutoSlugField
from utils.django.models import TimeStampedModel
from utils.python.constants import CHOICES_LEXERS

from apps.comments.models import Comment
from apps.comments.managers import CommentManager
from apps.comments.models_mixins import CommentsModelMixin
from apps.opinions.models import Opinion
from apps.opinions.managers import OpinionManager
from apps.opinions.models_mixins import OpinionsModelMixin
# from apps.flavours.models import Flavour
# from apps.flavours.managers import FlavourManager
# from apps.flavours.models_mixins import FlavourModelMixin
from apps.tags.models import Tag
from apps.tags.managers import TagManager
from apps.tags.models_mixins import TagsModelMixin

# from apps.visits.models import Visit

from .managers import SnippetManager
from .querysets import SnippetQuerySet


class Snippet(CommentsModelMixin, OpinionsModelMixin, TagsModelMixin, TimeStampedModel):
    """
    Model for snippet.
    """

    CHOICES_LEXERS = CHOICES_LEXERS

    name = models.CharField(
        _('name'), max_length=200, unique=True,
        validators=[MinLengthValidator(10)]
    )
    slug = ConfiguredAutoSlugField(populate_from='name', unique=True)
    lexer = models.CharField(_('lexer'), max_length=50, choices=CHOICES_LEXERS)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('user'),
        related_name='snippets', on_delete=models.CASCADE,
    )
    count_views = models.PositiveIntegerField(_('count views'), editable=False, default=0)
    description = models.TextField(_('decription'), validators=[MinLengthValidator(50)])
    code = models.TextField(_('code'), validators=[MinLengthValidator(5)])
    tags = models.ManyToManyField(
        Tag, verbose_name=_('tags'), related_name='snippets',
    )

    opinions = GenericRelation(Opinion, related_query_name='snippets')
    comments = GenericRelation(Comment, related_query_name='snippets')

    # managers
    objects = models.Manager()
    objects = SnippetManager.from_queryset(SnippetQuerySet)()

    opinions_manager = OpinionManager()

    tags_manager = TagManager()

    comments_manager = CommentManager()

    class Meta:
        db_table = 'snippets'
        verbose_name = _("Snippet")
        verbose_name_plural = _("Snippets")
        get_latest_by = 'created'
        ordering = ['created']

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):

        return reverse('snippets:detail', kwargs={'slug': self.slug})

    def get_admin_url(self):

        return get_admin_url(self)

    def related_snippets(self):
        """Deterniming a snippets, related with this snippet by tags and lexer."""

        raise NotImplementedError

        # get pks related objects by tags
        pks_related_snippets_by_tags = self._get_pks_related_objects_by_tags()

        # Analysis a lexer

        snippets_with_same_lexer = Snippet.objects.exclude(pk=self.pk).filter(lexer=self.lexer)
        pks_snippets_with_same_lexer = list(snippets_with_same_lexer.values_list('pk', flat=True))

        # join the snippets with same the lexer and snippets with related the tags
        all_pks_related_snippets = pks_related_snippets_by_tags + pks_snippets_with_same_lexer

        # count frequently similarity and return in descent order
        counter_related_snippets = collections.Counter(all_pks_related_snippets).most_common()

        # get only pk of each a snippet, without number
        only_pks_related_snippets = tuple(pk for pk, number in counter_related_snippets)

        # return related snippets as queryset
        related_snippets = Snippet.objects.filter(pk__in=only_pks_related_snippets)

        # correct order snippets
        sql = models.Case(*[models.When(pk=pk, then=pos) for pos, pk in enumerate(only_pks_related_snippets)])
        related_snippets = related_snippets.order_by(sql)
        return related_snippets

    def deny_commenting(self):
        """Deny commenting this snippet."""

        raise NotImplementedError
