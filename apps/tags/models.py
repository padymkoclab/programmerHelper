
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models

from mylabour.models import TimeStampedModel

from .managers import TagManager
from .querysets import TagQuerySet


class Tag(TimeStampedModel):
    """
    Model tags for another models
    """

    MIN_COUNT_TAGS_ON_OBJECT = 1
    MAX_COUNT_TAGS_ON_OBJECT = 5

    name = models.SlugField(
        _('name'),
        max_length=30,
        unique=True,
        allow_unicode=True,
        error_messages={'unique': _('Tag with this name already exists.')},
        help_text=_('Enter name tag. Attention: name of tag is case-sensetive.'),
    )

    class Meta:
        db_table = 'tags'
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        get_latest_by = 'date_modified'
        ordering = ['name']

    # managers
    objects = models.Manager()
    objects = TagManager.from_queryset(TagQuerySet)()

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('tags:tag', kwargs={'name': self.name})

    def count_usage_in_solutions(self):
        return self.__class__.objects.tags_with_count_solutions().get(pk=self.pk).count_usage_in_solutions

    def count_usage_in_articles(self):
        return self.__class__.objects.tags_with_count_articles().get(pk=self.pk).count_usage_in_articles

    def count_usage_in_snippets(self):
        return self.__class__.objects.tags_with_count_snippets().get(pk=self.pk).count_usage_in_snippets

    def count_usage_in_questions(self):
        return self.__class__.objects.tags_with_count_questions().get(pk=self.pk).count_usage_in_questions

    def count_usage_in_books(self):
        return self.__class__.objects.tags_with_count_books().get(pk=self.pk).count_usage_in_books

    def total_count_usage(self):
        return self.__class__.objects.tags_with_total_count_usage().get(pk=self.pk).total_count_usage
