
from django.db import models

from utils.django.sql import NullsLastQuerySet

from .constants import Badges


class BadgeQuerySet(models.QuerySet):
    """

    """

    def last_got_badges(self, count_last_getting=10):
        """Getting listing last getting badges of accounts."""

        pass


class UserBadgeQuerySet(NullsLastQuerySet):
    """

    """

    def users_with_total_count_badges(self):
        """ """

        return self.annotate(count_earned_badges=models.Count('badges', distinct=True))

    def users_with_count_gold_badges(self):
        """ """

        return self.annotate(count_gold_badges=models.functions.Coalesce(
            models.Sum(
                models.Case(
                    models.When(badges__badge__kind=Badges.Kind.GOLD.value, then=1),
                    output_field=models.PositiveIntegerField()
                )
            ), 0
        ))

    def users_with_count_silver_badges(self):
        """ """

        return self.annotate(count_silver_badges=models.functions.Coalesce(
            models.Sum(
                models.Case(
                    models.When(badges__badge__kind=Badges.Kind.SILVER.value, then=1),
                    output_field=models.PositiveIntegerField()
                )
            ), 0
        ))

    def users_with_count_bronze_badges(self):
        """ """

        return self.annotate(count_bronze_badges=models.functions.Coalesce(
            models.Sum(
                models.Case(
                    models.When(badges__badge__kind=Badges.Kind.BRONZE.value, then=1),
                    output_field=models.PositiveIntegerField()
                )
            ), 0
        ))

    def users_with_date_getting_latest_badge(self):
        """ """

        return self.annotate(date_latest_badge=models.Max('badges__created'))

    def users_with_pk_latest_badge(self):
        """ """

        return self.extra(
            select={
                'pk_latest_badge': """
                SELECT "badge_id"
                FROM
                    (
                    SELECT
                        "badge_id",
                        rank() OVER (PARTITION BY "user_id" ORDER BY "created" DESC)
                    FROM "badges_earnedbadge"
                    WHERE "users_user"."id" = "badges_earnedbadge"."user_id"
                    ) AS "A"
                WHERE "rank" = 1
                """
            }
        )

    def users_with_count_gold_silver_bronze_and_total_badges_and_date_getting_latest_badge(self):
        """ """

        self = self.users_with_total_count_badges()
        self = self.users_with_count_gold_badges()
        self = self.users_with_count_silver_badges()
        self = self.users_with_count_bronze_badges()
        self = self.users_with_date_getting_latest_badge()
        self = self.users_with_pk_latest_badge()

        return self
