
import random
import collections

from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from mylabour.models_fields import ConfiguredAutoSlugField
from apps.comments.models import Comment
from apps.opinions.models import Opinion
from apps.opinions.managers import OpinionManager
from apps.tags.managers import TagManager
from apps.favours.models import Favour
from apps.visits.models import Visit
from apps.tags.models import Tag
from apps.tags.model_mixins import RelatedObjectsByTags
from mylabour.models import TimeStampedModel
from mylabour.constants import CHOICES_LEXERS

from .managers import SnippetManager, PythonSnippetManager
from .querysets import SnippetQuerySet


class Snippet(RelatedObjectsByTags, TimeStampedModel):
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
    opinions_manager = OpinionManager()
    tags_manager = TagManager()
    # comments_manager = CommentManager()
    # favours_manager = FavourManager()

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

    def get_mark(self):
        """Get mark of snippet, on based opinions of users about it."""

        return self.__class__.objects.objects_with_marks().get(pk=self.pk).mark

    def get_count_views(self):
        return Visit.objects.get_count_visits_by_url(self.get_absolute_url)

    def show_users_given_bad_opinions(self):
        """Return the users determined this snippet as not useful."""

        return self.opinions.filter(is_useful=False).values_list('account__username', flat=True)

    def show_users_given_good_opinions(self):
        """Return the users determined this snippet as useful."""

        return self.opinions.filter(is_useful=True).values_list('account__username', flat=True)

    def related_snippets(self):
        """Deterniming a snippets, related with this snippet by tags and lexer."""

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

    def _select_another_lexer(self):
        """Select any one lexer of snippet, but not current."""

        # exclude current a lexer
        another_lexers = tuple(filter(lambda x: x[0] != self.lexer, Snippet.CHOICES_LEXERS))
        return random.choice(another_lexers)[0]

    def get_count_good_opinions(self):
        """Get count good opinions about this snippet."""

        return self.opinions.filter(is_useful=True).count()

    def get_count_bad_opinions(self):
        """Get count bad opinions about this snippet."""

        return self.opinions.filter(is_useful=False).count()

    def deny_commenting(self):
        """Deny commenting this snippet."""

        raise NotImplementedError
