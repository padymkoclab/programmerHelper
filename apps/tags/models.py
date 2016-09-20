
import itertools

from django.utils.text import slugify
from django.core.validators import MinLengthValidator
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models

from utils.django.models_utils import get_admin_url

from .managers import PurelyTagManager
from .querysets import PurelyTagQuerySet


class Tag(models.Model):
    """
    Model tags for another models
    """

    MIN_COUNT_TAGS_ON_OBJECT = 1
    MAX_COUNT_TAGS_ON_OBJECT = 5

    name = models.SlugField(
        _('name'), max_length=30,
        unique=True, allow_unicode=True,
        error_messages={'unique': _('Tag with this name already exists.')},
        help_text=_('Tag`s name is case-sensetive and must be as slug.')
    )
    description = models.CharField(
        _('Short description'), max_length=300,
        validators=[MinLengthValidator(10)]
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        get_latest_by = 'date_modified'
        ordering = ['name']
        # permissions = (('create_new_tags', _('You can create new tags.')),)

    # managers
    objects = models.Manager()
    objects = PurelyTagManager.from_queryset(PurelyTagQuerySet)()

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('tags:tag', kwargs={'name': self.name})

    def get_admin_url(self):
        return get_admin_url(self)

    def validate_unique(self, exclude=None):

        self.name = slugify(self.name, allow_unicode=True)
        super().validate_unique(exclude)

    def get_total_count_usage(self):
        """ """

        if hasattr(self, 'total_count_usage'):
            return self.total_count_usage

        return sum(
            getattr(self, related_field_name).count()
            for related_field_name in self.related_fields_names
        )
    get_total_count_usage.short_description = _('Total count usage')
    get_total_count_usage.admin_order_field = 'total_count_usage'

    @classmethod
    def _get_related_fields_names(cls):
        """ """

        return [
            field.name for field in cls._meta.get_fields()
            if type(field) == models.fields.reverse_related.ManyToManyRel
        ]

    @property
    def related_fields_names(self):
        return self._get_related_fields_names()

    def where_used(self):
        """ """

        querysets = (
            getattr(self, related_field_name).all()
            for related_field_name in self.related_fields_names
        )
        return tuple(itertools.chain.from_iterable(querysets))
