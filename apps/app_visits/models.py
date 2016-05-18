
import uuid

from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings


# class Visit(models.Model):
#     """

#     """

#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     name = models.CharField(_('Name'), max_length=200)
#     slug = AutoSlugField(_('Slug'), populate_from='name', unique=True, always_update=True, allow_unicode=True, db_index=True)
#     account = models.ManyToManyField(
#         settings.AUTH_USER_MODEL,
#         verbose_name=_('Account'),
#         related_name='visits',
#     )
#     date_visit = models.DateTimeField(_('Date visit'), auto_now_add=True)

#     class Meta:
#         db_table = 'visits'
#         verbose_name = _('Visit')
#         verbose_name_plural = _('Visits')
#         get_latest_by = 'date_visit'
#         ordering = ['date_visit']

#     objects = models.Manager()

#     def __str__(self):
#         return '{0.name}'.format(self)

#     def save(self, *args, **kwargs):
#         super(Visit, self).save(*args, **kwargs)

#     def get_absolute_url(self):
#         return reverse('app_:', kwargs={'slug': self.slug})
