
import uuid

from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings


class WebLink(models.Model):
    """
    Model tags for another models
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(
        _('Title'), max_length=200, unique=True, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    web_url = models.URLField(_('Web URL'))

    class Meta:
        db_table = 'web_links'
        verbose_name = _("Link in web")
        verbose_name_plural = _("Links in web")
        ordering = ['title']

    def __str__(self):
        return '{0.title}'.format(self)
