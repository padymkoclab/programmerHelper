
# from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

from utils.django.models_fields import ConfiguredAutoSlugField
from utils.django.models_utils import upload_image, get_admin_url
from utils.django.models import TimeStampedModel
from utils.django.validators import MinCountWordsValidator

from apps.comments.models import Comment
from apps.comments.models_mixins import CommentsModelMixin
from apps.marks.models import Mark
from apps.marks.models_mixins import MarksModelMixin
from apps.tags.models import Tag
from apps.tags.models_mixins import TagsModelMixin

from .managers import ArticleManager
from .querysets import ArticleQuerySet, SubsectionQuerySet


class Article(CommentsModelMixin, TagsModelMixin, MarksModelMixin, TimeStampedModel):
    """
    Model for article
    """

    MAX_COUNT_SUBSECTIONS = 10

    DRAFT = 'DRAFT'
    PUBLISHED = 'PUBLISHED'

    STATUS_ARTICLE = (
        (DRAFT, _('Draft')),
        (PUBLISHED, _('Published')),
    )

    ERROR_MSG_UNIQUE_TOGETHER_USER_AND_TITLE = _('This author already have article with this title.')

    def upload_image(instance, filename):
        return upload_image(instance, filename)

    title = models.CharField(
        _('Title'), max_length=200,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)],
    )
    slug = ConfiguredAutoSlugField(populate_from='title', unique_with=['user'])
    quotation = models.CharField(_('Quotation'), max_length=200, validators=[MinLengthValidator(10)])
    image = models.ImageField(_('Picture'), upload_to=upload_image, max_length=1000)
    heading = models.TextField(_('Heading'), validators=[MinCountWordsValidator(10)])
    conclusion = models.TextField(_('Conclusion'), validators=[MinCountWordsValidator(10)])
    status = models.CharField(_('Status'), max_length=10, choices=STATUS_ARTICLE, default=DRAFT)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('User'),
        related_name='articles', on_delete=models.CASCADE,
    )
    source = models.URLField(
        _('Source'), max_length=1000,
        null=True, default='',
        help_text=_('If this article is taken from another a web resource, please point URL to there.')
    )
    tags = models.ManyToManyField(
        Tag, related_name='articles', verbose_name=_('Tags'),
    )
    links = ArrayField(
        models.URLField(max_length=1000),
        size=10,
        verbose_name=_('Links'),
        help_text=_('Useful links'),
    )
    comments = GenericRelation(Comment, related_query_name='articles')
    marks = GenericRelation(Mark, related_query_name='articles')

    # managers
    objects = models.Manager()
    objects = ArticleManager.from_queryset(ArticleQuerySet)()

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        get_latest_by = 'date_added'
        ordering = ['date_added']
        unique_together = ['user', 'title']

    def __str__(self):
        return '{0.title}'.format(self)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:article', kwargs={'slug': self.slug})

    def get_admin_page_url(self):
        return get_admin_url(self)

    def unique_error_message(self, model_class, unique_check):
        if isinstance(self, model_class) and unique_check == ('user', 'title'):
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

        return sum([len(self.heading), len(self.conclusion), total_content_length])
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


class Subsection(TimeStampedModel):

    ERROR_MSG_UNIQUE_TOGETHER_ARTICLE_AND_TITLE = _('Subsection with this title already exists in this article.')

    article = models.ForeignKey(
        'Article',
        related_name='subsections',
        on_delete=models.CASCADE,
        verbose_name=_('Article'),
    )
    title = models.CharField(
        _('Title'),
        max_length=200,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)],
    )
    slug = ConfiguredAutoSlugField(populate_from='title', unique_with=['article'])
    content = models.TextField(_('Content'), validators=[MinLengthValidator(100)])

    class Meta:
        verbose_name = _("Subsection")
        verbose_name_plural = _("Subsections")
        ordering = ['article']
        unique_together = ['article', 'title']

    objects = models.Manager()
    objects = SubsectionQuerySet.as_manager()

    def __str__(self):
        return '{0.title}'.format(self)

    def unique_error_message(self, model_class, unique_check):
        if isinstance(self, model_class) and unique_check == ('article', 'title'):
            return self.ERROR_MSG_UNIQUE_TOGETHER_ARTICLE_AND_TITLE
        return super().unique_error_message(model_class, unique_check)
