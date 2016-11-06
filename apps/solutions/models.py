
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.django.models_utils import get_admin_url
from utils.django.models_fields import ConfiguredAutoSlugField
from utils.django.models import TimeStampedModel

from apps.comments.models import Comment
from apps.comments.managers import CommentManager
from apps.comments.mixins_models import CommentModelMixin
from apps.opinions.models import Opinion
from apps.opinions.managers import OpinionManager
from apps.opinions.mixins_models import OpinionModelMixin
from apps.tags.models import Tag
from apps.tags.managers import TagManager
from apps.tags.mixins_models import TagModelMixin

from .managers import SolutionManager
from .querysets import SolutionQuerySet


class Solution(CommentModelMixin, OpinionModelMixin, TagModelMixin, TimeStampedModel):
    """
    Model for solution.
    """

    problem = models.CharField(
        _('Title'), max_length=100, unique=True,
        validators=[
            MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)
        ],
        error_messages={'unique': _('Solution with this problem already exists.')}
    )
    slug = ConfiguredAutoSlugField(populate_from='problem', unique=True)
    body = models.TextField(_('Text solution'), validators=[MinLengthValidator(100)])
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='solutions',
        verbose_name=_('User'),
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='solutions',
        verbose_name=_('Tags'),
    )
    count_views = models.PositiveIntegerField(_('count views'), editable=False, default=0)

    comments = GenericRelation(Comment, related_query_name='solutions')
    opinions = GenericRelation(Opinion, related_query_name='solutions')

    objects = models.Manager()
    objects = SolutionManager.from_queryset(SolutionQuerySet)()

    comments_manager = CommentManager()
    tags_manager = TagManager()
    opinions_manager = OpinionManager()

    class Meta:
        verbose_name = _("Solution")
        verbose_name_plural = _("Solutions")
        ordering = ['problem']
        get_latest_by = 'updated'
        permissions = (("can_view_opinions_about_solutions", "Can view opinions about solutions"),)

    def __str__(self):
        return '{0.problem}'.format(self)

    def get_absolute_url(self):
        return reverse('solutions:solution', kwargs={'pk': self.pk, 'slug': self.slug})

    def get_admin_url(self):
        return get_admin_url(self)

    def related_solutions(self):
        """ """

        # analysis tags
        # analysis problem
        raise NotImplementedError
