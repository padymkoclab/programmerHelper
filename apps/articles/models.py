
# from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

from apps.comments.models import Comment
from apps.marks.models import Mark
from apps.tags.models import Tag
from mylabour.fields_db import ConfiguredAutoSlugField
from mylabour.models import TimeStampedModel
from mylabour.validators import MinCountWordsValidator

from .managers import ArticleManager
from .querysets import ArticleQuerySet


class Article(TimeStampedModel):
    """
    Model for article
    """

    MIN_COUNT_SUBSECTIONS = 1
    MAX_COUNT_SUBSECTIONS = 5

    DRAFT = 'DRAFT'
    PUBLISHED = 'PUBLISHED'

    STATUS_ARTICLE = (
        (DRAFT, _('Draft')),
        (PUBLISHED, _('Published')),
    )

    def upload_media(self, instance, filename):
        return '{account}/{model}/{slug}/{filename}'.format(
            filename=filename,
            slug=instance.slug,
            model=self.__class__._meta.verbose_name_plural,
            account=instance.account.get_short_name(),
        )

    title = models.CharField(
        _('Title'), max_length=200,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)],
    )
    slug = ConfiguredAutoSlugField(_('Slug'), populate_from='title', unique_with=['account'])
    quotation = models.CharField(_('Quotation'), max_length=200, validators=[MinLengthValidator(10)])
    picture = models.ImageField(_('Picture'), upload_to=upload_media, max_length=1000)
    header = models.TextField(_('Header'), validators=[MinCountWordsValidator(10)])
    conclusion = models.TextField(_('Conclusion'), validators=[MinCountWordsValidator(10)])
    status = models.CharField(_('Status'), max_length=10, choices=STATUS_ARTICLE, default=DRAFT)
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        related_name='articles',
        limit_choices_to={'is_active': True},
        on_delete=models.CASCADE,
    )
    source = models.URLField(
        _('Source'),
        max_length=1000,
        null=True,
        blank=True,
        help_text=_('If this article is taken from another a web resource, please point URL to there.')
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='articles',
        verbose_name=_('Tags'),
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
        db_table = 'articles'
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        get_latest_by = 'date_added'
        ordering = ['date_added']
        unique_together = ['account', 'title']

    def __str__(self):
        return '{0.title}'.format(self)

    def save(self, *args, **kwargs):
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:article', kwargs={'slug': self.slug})

    def get_admin_page_url(self):
        return reverse(
            'admin:{0}_{1}_change'.format(self._meta.app_label, self._meta.model_name),
            args=(self.pk,)
        )

    def unique_error_message(self, model_class, unique_check):
        if isinstance(self, model_class) and unique_check == ('account', 'title'):
            return _('This author already have article with this title.')
        return super(ArticleSubsection, self).unique_error_message(model_class, unique_check)

    def get_rating(self):
        return self.__class__.objects.articles_with_rating().get(pk=self.pk).rating
    get_rating.admin_order_field = 'rating'
    get_rating.short_description = _('Rating')

    def get_volume(self):
        return self.__class__.objects.articles_with_volume().get(pk=self.pk).volume
    get_volume.short_description = _('Volume')

    def related_articles(self):
        raise NotImplementedError
        # analysis tags
        # analysis title


class ArticleSubsection(TimeStampedModel):

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
    slug = ConfiguredAutoSlugField(_('Slug'), populate_from='title', unique_with=['article'])
    content = models.TextField(_('Content'), validators=[MinLengthValidator(100)])

    class Meta:
        db_table = 'articles_subsections'
        verbose_name = _("Subsection")
        verbose_name_plural = _("Subsections")
        ordering = ['article']
        unique_together = ['article', 'title']

    def __str__(self):
        return '{0.title}'.format(self)

    def unique_error_message(self, model_class, unique_check):
        if isinstance(self, model_class) and unique_check == ('article', 'title'):
            return _('Subsection with this title already exists in this article.')
        return super(ArticleSubsection, self).unique_error_message(model_class, unique_check)
