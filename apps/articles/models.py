
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

from utils.django.models_fields import ConfiguredAutoSlugField
from utils.django.functions_db import Round
from utils.django.models_utils import upload_image, get_admin_url
from utils.django.models import Timestampable, UUIDable, Viewable, Commentable
from utils.django.validators import MinCountWordsValidator

from apps.comments.models import Comment
from apps.comments.modelmixins import CommentModelMixin
from apps.comments.managers import CommentManager
from apps.tags.models import Tag
from apps.tags.modelmixins import TagModelMixin
from apps.tags.managers import TagManager

from .managers import ArticleManager, SubsectionManager, MarkManager


class Article(CommentModelMixin, TagModelMixin, Timestampable, UUIDable, Viewable, Commentable):
    """
    Model for article
    """

    MAX_COUNT_SUBSECTIONS = 10
    MAX_COUNT_LINKS = 10

    DRAFT = 'DRAFT'
    PUBLISHED = 'PUBLISHED'

    STATUS_ARTICLE = (
        (DRAFT, _('Draft')),
        (PUBLISHED, _('Published')),
    )

    ERROR_MSG_UNIQUE_TOGETHER_USER_AND_TITLE = _('This author already have article with this name.')

    def upload_image(instance, filename):
        return upload_image(instance, filename)

    name = models.CharField(
        _('name'), max_length=200,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)],
    )
    slug = ConfiguredAutoSlugField(populate_from='name', unique_with=['user'])
    quotation = models.CharField(_('quotation'), max_length=200, validators=[MinLengthValidator(10)])
    image = models.ImageField(_('image'), upload_to=upload_image, max_length=1000)
    header = models.TextField(_('header'), validators=[MinCountWordsValidator(10)])
    conclusion = models.TextField(_('conclusion'), validators=[MinCountWordsValidator(10)])
    status = models.CharField(_('status'), max_length=10, choices=STATUS_ARTICLE, default=DRAFT)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('user'),
        related_name='articles', on_delete=models.CASCADE,
    )
    source = models.URLField(
        _('source'), max_length=1000,
        null=True, default='',
        help_text=_('If this article is taken from another a web resource, please point URL to there.')
    )
    tags = models.ManyToManyField(
        Tag, related_name='articles', verbose_name=_('tags'),
    )
    links = ArrayField(
        models.URLField(max_length=1000),
        size=MAX_COUNT_LINKS,
        verbose_name=_('links'),
        help_text=_('Useful links'),
    )
    comments = GenericRelation(Comment, related_query_name='articles')

    # managers
    objects = models.Manager()
    objects = ArticleManager()
    comments_manager = CommentManager()
    tags_manager = TagManager()

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        get_latest_by = 'created'
        ordering = ('created', )
        unique_together = (('user', 'name'), )

    def __str__(self):
        return '{0.name}'.format(self)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:article', kwargs={'slug': self.slug, 'pk': self.pk})

    def get_admin_page_url(self):
        return get_admin_url(self)

    def unique_error_message(self, model_class, unique_check):
        if isinstance(self, model_class) and unique_check == ('user', 'name'):
            return self.ERROR_MSG_UNIQUE_TOGETHER_USER_AND_TITLE
        return super().unique_error_message(model_class, unique_check)

    def get_volume(self):
        """ """

        if hasattr(self, 'volume'):
            return self.volume

        subsections = self.subsections.subsections_with_length_of_content()
        total_content_length = subsections.aggregate(
            total_content_length=models.Sum('content_length')
        )['total_content_length']

        return sum([len(self.header), len(self.conclusion), total_content_length])
    get_volume.short_description = _('Volume')

    def get_count_subsections(self):
        """ """

        if hasattr(self, 'count_subsections'):
            return self.count_subsections

        return self.subsections.count()
    get_count_subsections.admin_order_field = 'count_subsections'
    get_count_subsections.short_description = _('Count subsections')

    def get_count_links(self):
        """ """

        if hasattr(self, 'count_links'):
            return self.count_links

        return len(self.links)
    get_count_links.admin_order_field = 'count_links'
    get_count_links.short_description = _('Count links')

    def get_count_marks(self):
        """ """

        if hasattr(self, 'count_marks'):
            return self.count_marks

        return self.marks.count()
    get_count_marks.admin_order_field = 'count_marks'
    get_count_marks.short_description = _('Count marks')

    def get_rating(self):
        """ """

        if hasattr(self, 'rating'):
            return self.rating

        return self.marks.aggregate(rating=Round(models.Avg('mark')))['rating']
    get_rating.admin_order_field = 'rating'
    get_rating.short_description = _('Rating')


class Subsection(Timestampable, UUIDable):

    ERROR_MSG_UNIQUE_TOGETHER_ARTICLE_AND_TITLE = _('Subsection with this name already exists in this article.')

    article = models.ForeignKey(
        'article',
        related_name='subsections',
        on_delete=models.CASCADE,
        verbose_name=_('Article'),
    )
    name = models.CharField(
        _('name'),
        max_length=200,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)],
    )
    slug = ConfiguredAutoSlugField(populate_from='name', unique_with=['article'])
    content = models.TextField(_('content'), validators=[MinLengthValidator(100)])

    class Meta:
        verbose_name = _("Subsection")
        verbose_name_plural = _("Subsections")
        ordering = ['article']
        unique_together = ['article', 'name']

    objects = models.Manager()
    objects = SubsectionManager()

    def __str__(self):
        return '{0.name}'.format(self)

    def unique_error_message(self, model_class, unique_check):
        if isinstance(self, model_class) and unique_check == ('article', 'name'):
            return self.ERROR_MSG_UNIQUE_TOGETHER_ARTICLE_AND_TITLE
        return super().unique_error_message(model_class, unique_check)


class Mark(Timestampable, UUIDable):
    """
    Model for keeping mark of other objects.
    """

    MIN_MARK = 1
    MAX_MARK = 5

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='marks', verbose_name=_('user'),
    )
    article = models.ForeignKey(
        Article, verbose_name=_('article'),
        on_delete=models.CASCADE, related_name='marks'
    )
    mark = models.SmallIntegerField(
        _('mark'), default=MIN_MARK,
        validators=[MinValueValidator(MIN_MARK), MaxValueValidator(MAX_MARK)]
    )

    objects = models.Manager()
    objects = MarkManager()

    class Meta:
        verbose_name = _('mark')
        verbose_name_plural = _('marks')
        permissions = (('can_view_marks', _('Can view marks')),)
        unique_together = (('user', 'article'), )
        get_latest_by = 'updated'
        ordering = ('created', )

    def __str__(self):
        return _('{0.mark}').format(self)

    def unique_error_message(self, model_class, unique_check):

        if model_class == type(self) and unique_check == ('user', 'article'):
            return _('User not allowed give mark about itself labour.')
        return super(Mark, self).unique_error_message(model_class, unique_check)
