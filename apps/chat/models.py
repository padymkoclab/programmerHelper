
import uuid

from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField


class Chat(models.Model):
    """

    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(
        _('Name'),
        unique=True,
        max_length=100,
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)],
    )
    slug = AutoSlugField(_('Slug'), populate_from='name', unique=True, always_update=True, allow_unicode=True, db_index=True)

    class Meta:
        db_table = 'chats'
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')
        ordering = ['name']

    objects = models.Manager()

    def __str__(self):
        return '{0.name'.format(self)

    def get_absolute_url(self):
        return reverse('chat:chat', kwargs={'slug': self.slug})
