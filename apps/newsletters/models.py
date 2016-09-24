
from django.template.defaultfilters import truncatechars
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models

from .managers import ManagerNewsletter


class Newsletter(models.Model):

    content = models.CharField(
        _('Content'),
        max_length=500,
        validators=[MinLengthValidator(25)]
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Newsletter")
        verbose_name_plural = _("Newsletters")
        get_latest_by = 'created'
        ordering = ['created']

    objects = models.Manager()
    objects = ManagerNewsletter()

    def __str__(self):
        return '{0.content}'.format(self)

    def truncated_content(self):
        """ """

        return truncatechars(self.content, 80)
    truncated_content.short_description = content.verbose_name
    truncated_content.admin_order_field = 'content'
