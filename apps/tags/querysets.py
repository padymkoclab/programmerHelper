
from django.db import models

from utils.django.models_utils import get_random_objects


class TagQuerySet(models.QuerySet):
    """
    Queryset for a manager, using for outside models.
    """

    def objects_with_count_tags(self):
        """Added to each object new field with count of tags of the a each object."""

        return self.annotate(count_tags=models.Count('tags', distinct=True))


class PurelyTagQuerySet(models.QuerySet):
    """
    Queryset for the model Tag
    """

    def random_tags(self, count):
        """ """

        return get_random_objects(self, count)

    def tags_with_total_count_usage(self):
        """ """

        related_fields_names = self.model._get_related_fields_names()

        kwargs = dict()
        for related_field_name in related_fields_names:
            related_field_name

            alias_name = 'count_{}'.format(related_field_name)
            annotation = models.Count(related_field_name, distinct=True)

            kwargs[alias_name] = annotation

        self = self.prefetch_related()
        self = self.annotate(**kwargs)

        CombinedExpression = None
        for alias in kwargs.keys():

            expression = models.F('{}'.format(alias))

            if CombinedExpression is None:
                CombinedExpression = expression
            else:
                CombinedExpression += expression

        condition = dict(total_count_usage=CombinedExpression)

        return self.annotate(**condition)
