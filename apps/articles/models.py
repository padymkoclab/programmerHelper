
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from model_utils.fields import StatusField, MonitorField
from model_utils import Choices

from apps.comments.models import Comment
from apps.scopes.models import Scope
from apps.tags.models import Tag
from apps.web_links.models import WebLink
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

    STATUS_ARTICLE = Choices(
        ('draft', _('Draft')),
        ('published', _('Published')),
    )

    title = models.CharField(
        _('Title'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = ConfiguredAutoSlugField(_('Slug'), populate_from='title', unique_with=['account'])
    quotation = models.CharField(_('Quotation'), max_length=200, validators=[MinLengthValidator(10)])
    picture = models.URLField(_('Picture'), max_length=1000)
    header = models.TextField(_('Header'), validators=[MinCountWordsValidator(5)])
    conclusion = models.TextField(_('Conclusion'), validators=[MinCountWordsValidator(5)])
    status = StatusField(verbose_name=_('Status'), choices_name='STATUS_ARTICLE', default=STATUS_ARTICLE.draft)
    status_changed = MonitorField(monitor='status', verbose_name=_('Status changed'))
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
    links = models.ManyToManyField(
        WebLink,
        related_name='articles',
        verbose_name=_('Links'),
        help_text=_('Useful links'),
    )
    comments = GenericRelation(Comment, related_query_name='articles')
    scopes = GenericRelation(Scope, related_query_name='articles')

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

    def get_rating(self):
        return self.__class__.objects.articles_with_rating().get(pk=self.pk).rating
    get_rating.admin_order_field = 'rating'
    get_rating.short_description = _('Rating')

    def get_volume(self):
        return self.__class__.objects.articles_with_volume().get(pk=self.pk).volume
    get_volume.short_description = _('Volume')


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
    number = models.PositiveSmallIntegerField(_('Number'), validators=[MinValueValidator(1)])
    content = models.TextField(_('Content'), validators=[MinLengthValidator(100)])

    class Meta:
        db_table = 'articles_subsections'
        verbose_name = _("Subsection")
        verbose_name_plural = _("Subsections")
        ordering = ['article', 'number']
        unique_together = ['article', 'title']

    def __str__(self):
        return '{0.title}'.format(self)

    def clean(self):
        # unique number of subsection for article
        if hasattr(self, 'article'):
            all_subsections = self.article.subsections
            if hasattr(self, 'pk'):
                all_subsections = all_subsections.exclude(pk=self.pk)
            if self.number in all_subsections.values_list('number', flat=True):
                raise ValidationError({
                    '__all__': _('Subsection with this number already exists.')
                })
        # adding count subsections
        # count_subsections_now = self.article.subsections.count() if  else self.article.subsections.count() + 1
        # if count_subsections_now > Article.MAX_COUNT_SUBSECTIONS:
        #     raise ValidationError({
        #         '__all__': _('Single article must be have no more than {0} subsections.').format(Article.MAX_COUNT_SUBSECTIONS),
        #     })
