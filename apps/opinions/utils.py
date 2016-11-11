
from django.db import models


def annotate_queryset_for_determinate_rating(queryset):
    """ """

    # subquery if using combination annotations and aggregations

    current_db_table = queryset.model._meta.db_table
    opinions_db_table = queryset.model._meta.get_field('opinions').related_model._meta.db_table
    queryset = queryset.extra(select={
        'rating': """
            SELECT
                SUM(
                    CASE
                        WHEN "{opinions_db_table}"."is_useful" = True THEN 1
                        WHEN "{opinions_db_table}"."is_useful" = False THEN -1
                    END
                )
            FROM "{opinions_db_table}"
            WHERE
                "{opinions_db_table}"."object_id" = "{current_db_table}"."id"
    """.format(current_db_table=current_db_table, opinions_db_table=opinions_db_table)
    })

    return queryset


def get_rating_instance(instance):

    opinions = instance.opinions.annotate(is_useful_int=models.Case(
        models.When(is_useful=True, then=1),
        models.When(is_useful=False, then=-1),
        output_field=models.IntegerField(),
    ))

    return opinions.aggregate(rating=models.Sum('is_useful_int'))['rating']
