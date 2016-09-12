
import random
import collections

from django.contrib.auth import get_user_model
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
from apps.opinions.models import Opinion
from apps.opinions.managers import OpinionManager
from apps.tags.models import Tag
from apps.tags.managers import TagManager

# from apps.visits.models import Visit
# from apps.tags.model_mixins import RelatedObjectsByTags

from .managers import SnippetManager
from .querysets import SnippetQuerySet


# class Snippet(RelatedObjectsByTags, TimeStampedModel):
class Snippet(TimeStampedModel):
    """
    Model for snippet.
    """

    CHOICES_LEXERS = CHOICES_LEXERS

    title = models.CharField(
        _('Title'), max_length=200, unique=True,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = ConfiguredAutoSlugField(populate_from='title', unique=True)
    lexer = models.CharField(_('Lexer'), max_length=50, choices=CHOICES_LEXERS)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('User'),
        related_name='snippets', on_delete=models.CASCADE,
    )
    description = models.TextField(_('Decription'), validators=[MinLengthValidator(50)])
    code = models.TextField(_('Code'), validators=[MinLengthValidator(5)])
    tags = models.ManyToManyField(
        Tag, verbose_name=_('Tags'), related_name='snippets',
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
        get_latest_by = 'date_added'
        ordering = ['date_added']

    def __str__(self):
        return '{0.title}'.format(self)

    def get_absolute_url(self):

        return reverse('snippets:detail', kwargs={'slug': self.slug})

    def get_admin_url(self):

        return get_admin_url(self)

    def get_count_comments(self):

        if hasattr(self, 'count_comments'):
            return self.count_comments

        return self.comments.count()
    get_count_comments.admin_order_field = 'count_comments'
    get_count_comments.short_description = _('Count comments')

    def get_count_opinions(self):

        if hasattr(self, 'count_opinions'):
            return self.count_opinions

        return self.opinions.count()
    get_count_opinions.admin_order_field = 'count_opinions'
    get_count_opinions.short_description = _('Count opinions')

    def get_count_tags(self):

        if hasattr(self, 'count_tags'):
            return self.count_tags

        return self.tags.count()
    get_count_tags.admin_order_field = 'count_tags'
    get_count_tags.short_description = _('Count tags')

    def get_rating(self):
        """Get mark of snippet, on based opinions of users about it."""

        if hasattr(self, 'rating'):
            return self.rating

        # convert boolean to integer
        self = self.opinions.annotate(
            is_useful_int=models.Case(
                models.When(is_useful=True, then=1),
                models.When(is_useful=False, then=-1),
                output_field=models.IntegerField()
            )
        )

        return self.aggregate(rating=models.functions.Coalesce(models.Sum('is_useful_int'), 0))['rating']
    get_rating.short_description = _('Rating')
    get_rating.admin_order_field = 'rating'

    def get_count_critics(self):
        """Get count good opinions about this snippet."""

        return self.get_critics().count()
    get_count_critics.short_description = _('Count critics')

    def get_count_supporters(self):
        """Get count bad opinions about this snippet."""

        return self.get_supporters().count()
    get_count_supporters.short_description = _('Count supporters')

    def get_critics(self):
        """Return the users determined this snippet as not useful."""

        user = self.opinions.filter(is_useful=False).values('user__pk')
        return get_user_model()._default_manager.filter(pk__in=user)
    get_critics.short_description = _('Critics')

    def get_supporters(self):
        """Return the users determined this snippet as useful."""

        user = self.opinions.filter(is_useful=True).values('user__pk')
        return get_user_model()._default_manager.filter(pk__in=user)
    get_supporters.short_description = _('Supporters')

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
