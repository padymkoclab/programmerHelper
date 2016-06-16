
import statistics

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.comments.models import Comment
from apps.opinions.models import Opinion
from apps.tags.models import Tag
from apps.web_links.models import WebLink
from mylabour.fields_db import ConfiguredAutoSlugField
from mylabour.models import TimeStampedModel

from .managers import SolutionCategoryManager
from .querysets import SolutionQuerySet, SolutionCategoryQuerySet


# Sort by count solutions

class SolutionCategory(TimeStampedModel):
    """
    Model for category of solution.
    """

    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True,
    )
    slug = ConfiguredAutoSlugField(_('Slug'), populate_from='name', unique=True)
    description = models.TextField(_('Description'), validators=[MinLengthValidator(100)])

    class Meta:
        db_table = 'solutions_categories'
        verbose_name = _("Category of solutions")
        verbose_name_plural = _("Categories of solutions")
        get_latest_by = 'date_added'
        ordering = ['name']

    objects = models.Manager()
    objects = SolutionCategoryManager.from_queryset(SolutionCategoryQuerySet)()

    def __str__(self):
        return '{0.name}'.format(self)

    def clean(self, *args, **kwargs):
        # make strip of description
        # self.description = self.description.strip()
        # self.name = self.name.strip()
        super(SolutionCategory, self).clean()

    def get_absolute_url(self):
        return reverse('solutions:category', kwargs={'pk': self.pk, 'slug': self.slug})

    def get_total_scope(self):
        """Getting total scope of category of solutions, on based scopes their solutions."""

        if not self.solutions.count():
            return None
        all_scopes_of_solutions = (solution.get_scope() for solution in self.solutions.iterator())
        mean_value = statistics.mean(all_scopes_of_solutions)
        return round(mean_value, 4)
    get_total_scope.short_description = _('Total scope')
    get_total_scope.admin_order_field = 'total_scope'

    def get_latest_activity(self):
        """Determined date and time last activity in category of solution,
        on based latest datetime chages in itself category or their solutions."""

        return self.__class__.objects.categories_with_latest_activity().get(pk=self.pk).latest_activity
    get_latest_activity.short_description = _('Latest activity')
    get_latest_activity.admin_order_field = 'latest_activity'


class Solution(TimeStampedModel):
    """
    Model for solution.
    """

    title = models.CharField(
        _('Title'), max_length=100, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = ConfiguredAutoSlugField(_('Slug'), populate_from='title', unique_with=['category'])
    body = models.TextField(_('Text solution'), validators=[MinLengthValidator(100)])
    category = models.ForeignKey(
        'SolutionCategory',
        on_delete=models.CASCADE,
        related_name='solutions',
        verbose_name=_('Category'),
    )
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='solutions',
        verbose_name=_('Author'),
        on_delete=models.CASCADE,
        limit_choices_to={'is_active': True}
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='solutions',
        verbose_name=_('Tags'),
    )
    links = models.ManyToManyField(
        WebLink,
        related_name='solutions',
        verbose_name=_('Useful links'),
    )

    comments = GenericRelation(Comment, related_query_name='solutions')
    opinions = GenericRelation(Opinion, related_query_name='solutions')

    # managers
    objects = models.Manager()
    objects = SolutionQuerySet.as_manager()

    class Meta:
        db_table = 'solutions'
        verbose_name = _("Solution")
        verbose_name_plural = _("Solutions")
        ordering = ['category', 'title']
        unique_together = ['title', 'category']
        get_latest_by = 'date_modified'
        permissions = (("can_view_opinions_about_solutions", "Can view opinions about solutions"),)

    def __str__(self):
        return '{0.title}'.format(self)

    def get_absolute_url(self):
        return reverse('solutions:solution', kwargs={'pk': self.pk, 'slug': self.slug})

    def unique_error_message(self, model_class, unique_check):
        if isinstance(self, model_class) and unique_check == ('title', 'category'):
            return _('Solution with this title already exists in this category of solutions.')
        return super(Solution, self).unique_error_message(model_class, unique_check)

    def get_scope(self):
        """Getting scope of solution on based their opinions."""

        return self.__class__.objects.solutions_with_scopes().get(pk=self.pk).scope
    get_scope.short_description = _('Scope')
    get_scope.admin_order_field = 'scope'

    def get_quality(self):
        """Getting quality of solution on based its scope."""

        # this is approved solution and so, it had sign "Sign quality"
        return self.__class__.objects.solutions_with_qualities().get(pk=self.pk).quality
    get_quality.short_description = _('Quality')
    get_quality.admin_order_field = 'scope'

    def get_quality_detail(self):
        """Get detail about quality of solution, namely: name, description and color."""

        quality = self.get_quality()
        if quality == 'Approved':
            return _('Approved quality solution, tells about what solution is have many possitive opinions from users.')
        elif quality == 'Good':
            return _('Good quality solution, tells about what solution is have more possitive opinions of users. than negative.')
        elif quality == 'Vague':
            return _('Vague quality solution, tells about what solution is have not clear definition of quality.')
        elif quality == 'Bad':
            return _('Bad quality solution, tells about what solution is have more negative opinions of users, than possitive.')
        elif quality == 'Heinously':
            return _('Heinously quality solution, tells about what solution is have many negative opinions from users.')

    def critics_of_solution(self):
        """Determination users given negative opinions about solution."""

        return get_user_model().objects.filter(pk__in=self.opinions.filter(is_useful=False).values('account__pk'))

    def supporters_of_solution(self):
        """Determination users given possitive opinions about solution."""

        return get_user_model().objects.filter(pk__in=self.opinions.filter(is_useful=True).values('account__pk'))
