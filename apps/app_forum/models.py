
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from model_utils import Choices
from model_utils.models import MonitorField, StatusField
from autoslug import AutoSlugField

from mylabour.models import TimeStampedModel


class ForumTheme(TimeStampedModel):
    """

    """

    name = models.CharField(
        _('Name'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(_('Slug'), populate_from='name', unique=True, always_update=True, db_index=True, allow_unicode=True)
    description = models.TextField(_('Description'))

    class Meta:
        db_table = 'forum_themes'
        verbose_name = ("Theme")
        verbose_name_plural = _("Themes")
        ordering = ['name']
        get_latest_by = 'date_modified'

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('app_forum:theme', kwargs={'slug': self.slug})

    # last activity


class ForumTopic(TimeStampedModel):
    """

    """

    CHOICES_STATUS = Choices(
        ('closed', _('Closed')),
        ('open', _('Open')),
    )

    name = models.CharField(
        _('Name'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(_('Slug'), populate_from='name', unique=True, always_update=True, db_index=True, allow_unicode=True)
    theme = models.ForeignKey('ForumTheme', verbose_name=_('Theme'), related_name='topics', on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        related_name='topics',
        on_delete=models.PROTECT,
        limit_choices_to={'is_superuser': True, 'is_active': True},
    )
    description = models.TextField(_('Description'))
    status = StatusField(verbose_name=_('Status'), choices_name='CHOICES_STATUS', default=CHOICES_STATUS.open)
    status_changed = MonitorField(verbose_name=_('Status changed'), monitor='status')
    views = models.IntegerField(_('Count views'), default=0, editable=False)

    class Meta:
        db_table = 'forum_topics'
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')
        order_with_respect_to = 'theme'
        unique_together = ['slug', 'theme']
        get_latest_by = 'date_modified'

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('app_forum:topic', kwargs={'slug': self.slug})

    # date_last_activity


class ForumPost(TimeStampedModel):
    """

    """

    topic = models.ForeignKey(
        'ForumTopic',
        verbose_name=_('Topic'),
        on_delete=models.CASCADE,
        related_name='posts',
        limit_choices_to={'status': ForumTopic.CHOICES_STATUS.open},
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        related_name='posts',
        on_delete=models.DO_NOTHING,
        limit_choices_to={'is_active': True},
    )
    content = models.TextField(_('Content'))
    # is_published
    # is_hidden

    class Meta:
        db_table = 'forum_posts'
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        order_with_respect_to = 'topic'
        get_latest_by = 'date_modified'

    def __str__(self):
        return 'Post from {0.author} in topic "{0.topic}"'.format(self)
