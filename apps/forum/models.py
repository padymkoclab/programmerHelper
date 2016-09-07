
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField

from utils.django.models import TimeStampedModel

from .managers import ForumTopicManager, ForumTopicQuesrySet


class ForumSection(TimeStampedModel):
    """

    """

    name = models.CharField(
        _('Name'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(_('Slug'), populate_from='name', unique=True, always_update=True, db_index=True, allow_unicode=True)
    description = models.TextField(_('Description'))

    class Meta:
        db_table = 'forum_themes'
        verbose_name = ("Section")
        verbose_name_plural = _("Sections")
        ordering = ['name']
        get_latest_by = 'date_modified'

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('forum:theme', kwargs={'slug': self.slug})

    def last_activity(self):
        return self.topics.latest().date_modified
    last_activity.short_description = _('Last activity')

    def get_count_posts(self):
        result = self.topics.annotate(count_posts=models.Count('posts')).aggregate(total_count_posts=models.Sum('count_posts'))
        return result['total_count_posts']
    get_count_posts.admin_order_field = 'count_topics'  # annotate in admin.py file
    get_count_posts.short_description = _('Count posts')

    def count_active_users(self):
        """Count users posted in topic of theme"""
        result = set()
        for topic in self.topics.iterator():
            result.update(topic.get_active_users())
        return len(result)
    count_active_users.short_description = _('Active users')


class ForumTopic(TimeStampedModel):
    """

    """

    CLOSED = 'CLOSED'
    OPEN = 'OPEN'

    CHOICES_STATUS = (
        (CLOSED, _('Closed')),
        (OPEN, _('Open')),
    )

    name = models.CharField(
        _('Name'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(_('Slug'), populate_from='name', unique_with=['theme'], always_update=True, db_index=True, allow_unicode=True)
    theme = models.ForeignKey('ForumSection', verbose_name=_('Theme'), related_name='topics', on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        related_name='topics',
        on_delete=models.CASCADE,
        limit_choices_to={'is_superuser': True, 'is_active': True},
    )
    description = models.TextField(_('Description'))
    status = models.CharField(_('Status'), max_length=10, choices=CHOICES_STATUS, default=OPEN)
    views = models.IntegerField(_('Count views'), default=0, editable=False)

    # managers
    objects = models.Manager()
    objects = ForumTopicManager.from_queryset(ForumTopicQuesrySet)()

    class Meta:
        db_table = 'forum_topics'
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')
        ordering = ['theme', 'date_added']
        unique_together = ['name', 'theme']
        get_latest_by = 'date_modified'

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('forum:topic', kwargs={'slug': self.slug})

    def last_activity(self):
        return self.posts.latest().date_modified
    last_activity.short_description = _('Last activity')

    def get_active_users(self):
        """Return set users posted in this topic"""
        return frozenset(self.posts.values_list('author', flat=True))

    def count_active_users(self):
        """Count users posted in topic"""
        active_users = self.get_active_users()
        return len(active_users)
    count_active_users.short_description = _('Active users')


class ForumPost(TimeStampedModel):
    """ForumManager

    """

    topic = models.ForeignKey(
        'ForumTopic',
        verbose_name=_('Topic'),
        on_delete=models.CASCADE,
        related_name='posts',
        limit_choices_to={'status': ForumTopic.OPEN},
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        related_name='posts',
        on_delete=models.CASCADE,
        limit_choices_to={'is_active': True},
    )
    content = models.TextField(_('Content'))
#     # is_published
#     # is_hidden

    class Meta:
        db_table = 'forum_posts'
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['topic', 'date_modified']
        get_latest_by = 'date_modified'

    def __str__(self):
        return 'Post from {0.author} in topic "{0.topic}"'.format(self)
