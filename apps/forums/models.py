
import uuid

from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.db import models
from django.conf import settings

from utils.django.models import TimeStampedModel
from utils.django.models_fields import ConfiguredAutoSlugField
from utils.django.models_utils import upload_image

from .managers import ForumManager, TopicManager


class Section(models.Model):
    """

    """

    def upload_image(instance, filename):
        return upload_image(instance, filename)

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(_('Name'), max_length=80, unique=True)
    groups = models.ManyToManyField(
        Group, blank=True,
        verbose_name=_('Groups'),
        help_text=_('Only users from these groups can see this section')
    )
    position = models.PositiveSmallIntegerField(
        _('Position'), unique=True,
        validators=[MinValueValidator(1)]
    )
    image = models.ImageField(_('Image'), upload_to=upload_image)

    class Meta:
        ordering = ['position']
        verbose_name = "Section"
        verbose_name_plural = "Sections"

    def __str__(self):
        return '{0.name}'.format(self)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def posts(self):
        return Post.objects.filter().select_related()

    @property
    def topics(self):
        return Topic.objects.filter().select_related()

    def get_count_forums(self):
        """ """

        if hasattr(self, 'count_forums'):
            return self.count_forums

        return self.forums.count()
    get_count_forums.short_description = _('Count forums')
    get_count_forums.admin_order_field = 'count_forums'

    def has_access(self, user):

        if user.superuser:
            return True

        if self.groups.exists():
            if user.is_authenticated():
                if not self.groups.filter(user__pk=user.pk).exists():
                    return True
            else:
                return False
        return True


class Forum(models.Model):
    """

    """

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(
        _('Name'), max_length=200,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = ConfiguredAutoSlugField(populate_from='name', unique_with=['section'])
    section = models.ForeignKey(
        'Section', related_name='forums',
        on_delete=models.CASCADE, verbose_name=_('Section')
    )
    description = models.TextField(
        _('Description'),
        validators=[MinLengthValidator(10)]
    )
    moderators = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('Moderator'))
    date_modified = models.DateTimeField(_('Date modified'), auto_now=True)

    objects = models.Manager()
    objects = ForumManager()

    class Meta:
        verbose_name = ("Forum")
        verbose_name_plural = _("Forums")
        ordering = ['name']
        get_latest_by = 'date_modified'
        unique_together = (('section', 'name'))

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('forum:theme', kwargs={'slug': self.slug})

    @property
    def posts(self):
        return Post.objects.filter().select_related()

    @property
    def head(self):
        try:
            self.topic.first()
        except Topic.DoesNotExists:
            return

    def latest_post(self):
        """ """

        return self.topics.latest()
    latest_post.short_description = _('Last post')

    def get_count_topics(self):
        """ """

        if hasattr(self, 'count_topics'):
            return self.count_topics

        return self.topics.count()
    get_count_topics.admin_order_field = 'count_topics'
    get_count_topics.short_description = _('Count topics')

    def get_total_count_posts(self):
        """ """

        if hasattr(self, 'total_count_topics'):
            return self.total_count_topics

        topics = self.topics.topics_with_count_posts()
        return topics.aggregate(total_count_posts=models.Sum('count_posts'))['total_count_posts']
    get_total_count_posts.short_description = _('Total count posts')
    get_total_count_posts.admin_order_field = 'total_count_topics'

    def count_active_users(self):
        """Count users posted in topic of theme"""
        result = set()
        for topic in self.topics.iterator():
            result.update(topic.get_active_users())
        return len(result)
    count_active_users.short_description = _('Active users')


class Topic(TimeStampedModel):
    """

    """

    CLOSED = 'CLOSED'
    OPEN = 'OPEN'

    CHOICES_STATUS = (
        (CLOSED, _('Closed')),
        (OPEN, _('Open')),
    )

    subject = models.CharField(
        _('Name'), max_length=200,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = ConfiguredAutoSlugField(populate_from='subject', unique_with=['forum'])
    forum = models.ForeignKey(
        'Forum', verbose_name=_('Forum'),
        related_name='topics', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('User'),
        related_name='topics', on_delete=models.CASCADE,
    )
    description = models.TextField(_('Description'))
    status = models.CharField(_('Status'), max_length=10, choices=CHOICES_STATUS, default=OPEN)
    views = models.IntegerField(_('Count views'), default=0, editable=False)
    is_sticky = models.BooleanField(_('Is sticky'), default=False)
    is_closed = models.BooleanField(_('Is closed?'), default=False)

    # managers
    objects = models.Manager()
    objects = TopicManager()

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')
        ordering = ['forum', 'date_added']
        unique_together = ['subject', 'forum']
        get_latest_by = 'date_modified'

    def __str__(self):
        return '{0.subject}'.format(self)

    def get_absolute_url(self):
        return reverse('forum:topic', kwargs={'slug': self.slug})

    def last_activity(self):
        return self.posts.latest().date_modified
    last_activity.short_description = _('Last activity')

    def get_active_users(self):
        """Return set users posted in this topic"""
        return frozenset(self.posts.values_list('user', flat=True))

    def count_active_users(self):
        """Count users posted in topic"""
        active_users = self.get_active_users()
        return len(active_users)
    count_active_users.short_description = _('Active users')


class Post(TimeStampedModel):
    """

    """

    MARKDOWN = 'markdown'

    MARKUP_CHOICES = (
        (MARKDOWN, _('Markdown')),
    )

    topic = models.ForeignKey(
        'Topic', verbose_name=_('Topic'),
        on_delete=models.CASCADE, related_name='posts',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('User'),
        related_name='posts', on_delete=models.CASCADE,
    )
    markup = models.CharField(_('Markup'), max_length=25, choices=MARKUP_CHOICES)
    body = models.TextField(_('Message'))
    body_html = models.TextField(_('Message (HTML version)'))
    user_ip = models.GenericIPAddressField(_('User IP'), blank=True, null=True)
#     # is_published
#     # is_hidden

    class Meta:
        db_table = 'forum_posts'
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['topic', 'date_modified']
        get_latest_by = 'date_modified'

    def __str__(self):
        return 'Post from {0.user} in topic "{0.topic}"'.format(self)
