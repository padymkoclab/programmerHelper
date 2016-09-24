
import uuid

from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.template.defaultfilters import truncatechars
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.db import models
from django.conf import settings

from utils.django.datetime_utils import convert_date_to_django_date_format
from utils.django.models import TimeStampedModel
from utils.django.models_fields import ConfiguredAutoSlugField, MarkupField
from utils.django.models_utils import get_admin_url

from .managers import SectionManager, ForumManager, TopicManager, PostManager


class Section(models.Model):
    """

    """

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(_('Name'), max_length=80, unique=True, validators=[MinLengthValidator(5)])
    groups = models.ManyToManyField(
        Group, blank=True,
        verbose_name=_('Groups'),
        help_text=_('Only users from these groups can see this section')
    )
    position = models.PositiveSmallIntegerField(
        _('Position'), unique=True,
        validators=[MinValueValidator(1)]
    )

    objects = models.Manager()
    objects = SectionManager()

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

    def get_total_count_topics(self):
        """ """

        if hasattr(self, 'total_count_topics'):
            return self.total_count_topics

        forums = self.forums.forums_with_count_topics()
        return forums.aggregate(sum=models.Sum('count_topics'))['sum']
    get_total_count_topics.short_description = _('Total count topics')
    get_total_count_topics.admin_order_field = 'total_count_topics'

    def get_total_count_posts(self):
        """ """

        if hasattr(self, 'total_count_posts'):
            return self.total_count_posts

        return self.forums.count()
    get_total_count_posts.short_description = _('Total count posts')
    get_total_count_posts.admin_order_field = 'total_count_posts'

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


class Forum(TimeStampedModel):
    """

    """

    name = models.CharField(
        _('Name'), max_length=200,
        validators=[MinLengthValidator(5)]
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

    objects = models.Manager()
    objects = ForumManager()

    class Meta:
        verbose_name = ("Forum")
        verbose_name_plural = _("Forums")
        ordering = ['name']
        get_latest_by = 'updated'
        unique_together = (('section', 'name'))

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('forums:forum', kwargs={'slug': self.slug})

    def get_admin_url(self):
        return get_admin_url(self)

    @property
    def posts(self):
        return Post.objects.filter().select_related()

    @property
    def head(self):
        try:
            self.topic.first()
        except Topic.DoesNotExists:
            return

    def get_latest_post(self):
        """ """

        latest_post = None

        for topic in self.topics.iterator():
            post = topic.get_latest_post()
            if post is not None:
                if latest_post is None:
                    latest_post = post
                else:
                    field_for_latest = Post._meta.get_latest_by

                    value_latest_post = getattr(latest_post, field_for_latest)
                    value_post = getattr(post, field_for_latest)

                    if value_post > value_latest_post:
                        latest_post = post
    get_latest_post.short_description = _('Latest post')

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
        return topics.aggregate(
            total_count_posts=models.functions.Coalesce(
                models.Sum('count_posts'), 0
            )
        )['total_count_posts']
    get_total_count_posts.short_description = _('Total count posts')
    get_total_count_posts.admin_order_field = 'total_count_posts'

    def get_count_active_users(self):
        """ """

        users = set()
        for user1, user2 in self.topics.values_list('user', 'posts__user'):
            users.add(user1)
            users.add(user2)

        return len(users)
    get_count_active_users.short_description = _('Count active users')
    get_count_active_users.admin_order_field = 'count_active_users'

    def display_details_latest_post(self):
        """ """

        latest_post = self.get_latest_post()

        if latest_post is None:
            return

        latest_post_updated = convert_date_to_django_date_format(latest_post.updated)

        return format_html(_('by {}<br />{}'), latest_post.user, latest_post_updated)
    display_details_latest_post.short_description = _('Latest post')


class Topic(TimeStampedModel):
    """

    """

    subject = models.CharField(_('Subject'), max_length=200, validators=[MinLengthValidator(5)])
    slug = ConfiguredAutoSlugField(populate_from='subject', unique_with=['forum'])
    forum = models.ForeignKey(
        'Forum', verbose_name=_('Forum'),
        related_name='topics', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('User'),
        related_name='topics', on_delete=models.CASCADE,
    )
    views = models.IntegerField(_('Count views'), default=0, editable=False)
    is_sticky = models.BooleanField(_('Is sticky'), default=False)
    is_opened = models.BooleanField(_('Is opened?'), default=True)

    # managers
    objects = models.Manager()
    objects = TopicManager()

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')
        ordering = ['-is_sticky', 'forum', '-created']
        unique_together = ['subject', 'forum']
        get_latest_by = 'updated'

    def __str__(self):
        return '{0.subject}'.format(self)

    def get_absolute_url(self):
        return reverse('forums:topic', kwargs={'slug': self.slug})

    def get_admin_url(self):
        return get_admin_url(self)

    @property
    def head(self):
        """ """

        return self.posts.select_related().order_by('created').first()

    def get_count_posts(self):
        """ """

        if hasattr(self, 'count_posts'):
            return self.count_posts

        return self.posts.count()
    get_count_posts.admin_order_field = 'count_posts'
    get_count_posts.short_description = _('Count posts')

    def get_count_active_users(self):
        """Return set users posted in this topic"""

        return self.posts.values('user').distinct().count()

    def count_active_users(self):
        """Count users posted in topic"""
        active_users = self.get_active_users()
        return len(active_users)
    count_active_users.short_description = _('Active users')
    count_active_users.admin_order_field = 'count_active_users'

    def get_latest_post(self):
        """ """

        try:
            return self.posts.latest()
        except Post.DoesNotExist:
            return

    def display_details_latest_post(self):
        """ """

        latest_post = self.get_latest_post()

        if latest_post is None:
            return

        latest_post_updated = convert_date_to_django_date_format(latest_post.updated)

        return format_html(_('by {}<br />{}'), latest_post.user, latest_post_updated)
    display_details_latest_post.short_description = _('Latest post')


class Post(TimeStampedModel):
    """

    """

    topic = models.ForeignKey(
        'Topic', verbose_name=_('Topic'),
        on_delete=models.CASCADE, related_name='posts',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('User'),
        related_name='posts', on_delete=models.CASCADE,
    )
    markup = MarkupField(fill_from='content', fill_to='content_html')
    content = models.TextField(_('Content'))
    content_html = models.TextField(_('Content (HTML)'))
    user_ip = models.GenericIPAddressField(_('User IP'), blank=True, null=True)

    objects = models.Manager()
    objects = PostManager()

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['topic', 'created']
        get_latest_by = 'created'

    def __str__(self):
        return truncatechars(self.content, 100)

    def display_content_html(self):
        """ """

        return mark_safe(self.content_html)
    display_content_html.short_description = content_html.verbose_name
