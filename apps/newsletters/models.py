
from django.template.defaultfilters import truncatechars
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models

from utils.django.models import Creatable

from .managers import ManagerNewsletter


class Newsletter(Creatable):

    content = models.CharField(
        _('content'),
        max_length=500,
        validators=[MinLengthValidator(25)]
    )

    class Meta:
        verbose_name = _("newsletter")
        verbose_name_plural = _("newsletters")
        get_latest_by = 'created'
        ordering = ['created']
        # may be need unique_together ((created, content))

    objects = models.Manager()
    objects = ManagerNewsletter()

    def __str__(self):
        return '{0.content}'.format(self)

    def truncated_content(self):
        """ """

        return truncatechars(self.content, 80)
    truncated_content.short_description = content.verbose_name
    truncated_content.admin_order_field = 'content'

    @classmethod
    def from_db(cls, db, field_names, values):
        raise ValueError
        instance = super(Newsletter, cls).from_db(cls, db, field_names, values)
        import ipdb; ipdb.set_trace()
        return instance

    def save(self, *args, **kwargs):
        # import ipdb; ipdb.set_trace()
        raise TypeError
        super(Newsletter, self).save(*args, **kwargs)
