
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField

from mylabour.models import TimeStampedModel, LikeUserModel


# Are you agree?

class ProgrammingCategory(TimeStampedModel):
    """

    """

    name = models.CharField(
        _('Name'), max_length=200, unique=True, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True, db_index=True, allow_unicode=True)
    description = models.TextField(_('Description'))
    picture = models.URLField(_('Picture'), max_length=1000)
    views = models.IntegerField(_('Count views'), default=0, editable=False)

    class Meta:
        db_table = 'programming_categories'
        verbose_name = _("Programming category")
        verbose_name_plural = _("Programming categories")
        get_latest_by = 'date_modified'
        ordering = ['name']

    def __str__(self):
        return '{0.name}'.format(self)

    def get_absolute_url(self):
        return reverse('app_programming_utilities:programming_category', kwargs={'slug': self.slug})

# show comments (default hide)


class ProgrammingUtility(TimeStampedModel):
    """

    """

    name = models.CharField(
        _('Name'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    description = models.TextField(_('Description'))
    picture = models.URLField(_('Picture'), max_length=1000)
    category = models.ForeignKey(
        'ProgrammingCategory',
        related_name='programming_utilities',
        verbose_name=_('Category'),
        on_delete=models.CASCADE,
    )
    web_link = models.URLField(_('Web link'))
    opinions = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='opinions_about_utilities',
        verbose_name=_('Opinions'),
        through='OpinionAboutProgrammingUtility',
        through_fields=['utility', 'user']
    )
    comments = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='comments_about_utilities',
        verbose_name=_('Comments'),
        through='ProgrammingUtilityComment',
        through_fields=['utility', 'author']
    )

    class Meta:
        db_table = 'programming_utilities'
        verbose_name = _("Utility")
        verbose_name_plural = _("Utilities")
        ordering = ['category', 'name']
        unique_together = ['name', 'category']

    def __str__(self):
        return '{0.name}'.format(self)


class ProgrammingUtilityComment(TimeStampedModel):
    """

    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name=_('Author'))
    utility = models.ForeignKey('ProgrammingUtility', on_delete=models.CASCADE, verbose_name=_('Utility'))

    class Meta:
        db_table = 'programming_utilities_comments'
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['utility', 'date_modified']

    objects = models.Manager()

    def __str__(self):
        return 'Commen from "{0.user}" on utility "{0.utility}"'.format(self)


class OpinionAboutProgrammingUtility(LikeUserModel):
    """

    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name=_('User'))
    utility = models.ForeignKey('ProgrammingUtility', on_delete=models.CASCADE, verbose_name=_('Utility'))

    class Meta(LikeUserModel.Meta):
        db_table = 'programming_utilities_opinions'
        verbose_name = _('Opinion')
        verbose_name_plural = _('Opinions')
        unique_together = ['user', 'utility']

    objects = models.Manager()

    def __str__(self):
        return 'Opnion of user "{0.user}" on utility "{0.utility}"'.format(self)

    def save(self, *args, **kwargs):
        super(OpinionAboutProgrammingUtility, self).save(*args, **kwargs)
