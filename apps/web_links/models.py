
import itertools
import uuid

from django.template.defaultfilters import truncatechars
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from .querysets import WebLinkQuerySet
from .managers import WebLinkManager


class WebLink(models.Model):
    """
    Model links for another models
    """

    MAX_COUNT_WEBLINKS_ON_OBJECT = 10

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(
        _('Title'),
        max_length=200,
        blank=True,
        default='',
        validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)],
    )
    url = models.URLField(_('URL'), help_text=_('URL will be saved in lowercase.'))

    objects = models.Manager()
    objects = WebLinkManager.from_queryset(WebLinkQuerySet)()

    class Meta:
        db_table = 'web_links'
        verbose_name = _("Link in web")
        verbose_name_plural = _("Links in web")
        ordering = ['url']

    def __str__(self):
        if self.title == '':
            url = truncatechars(self.url, 50)
            return '{0}'.format(url)
        return '{0.title}'.format(self)

    def save(self, *args, **kwargs):
        self.url = self.url.lower()
        super(WebLink, self).save(*args, **kwargs)

    def get_status(self):
        """Return status web link: if it worked - True, otherwise (is broken) - False."""

        return self.__class__.objects.weblinks_with_status().get(pk=self.pk).is_active
    get_status.short_description = _('Is active')
    get_status.admin_order_field = 'is_active'
    get_status.boolean = True

    def where_used(self):
        """Return string representation related with weblink object."""

        solutions_and_articles = tuple(itertools.chain.from_iterable([self.solutions.all(), self.articles.all()]))
        return solutions_and_articles
