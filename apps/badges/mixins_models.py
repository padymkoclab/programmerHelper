
from django.utils.translation import ugettext_lazy as _

from .constants import Badges
from .models import Badge


class BadgeModelMixin(object):
    """

    """

    def has_badge(self, badge):

        return self.badges.filter(badge=badge).exists()

    def get_count_earned_badges(self):

        if hasattr(self, 'count_earned_badges'):
            return self.count_earned_badges

        return self.get_earned_badges().count()
    get_count_earned_badges.short_description = _('Count badges')
    get_count_earned_badges.admin_order_field = 'count_earned_badges'

    def get_count_gold_badges(self):

        if hasattr(self, 'count_gold_badges'):
            return self.count_gold_badges

        return self.get_gold_badges().count()
    get_count_gold_badges.short_description = _('Count gold badges')
    get_count_gold_badges.admin_order_field = 'count_gold_badges'

    def get_count_silver_badges(self):

        if hasattr(self, 'count_silver_badges'):
            return self.count_silver_badges

        return self.get_silver_badges().count()
    get_count_silver_badges.short_description = _('Count silver badges')
    get_count_silver_badges.admin_order_field = 'count_silver_badges'

    def get_count_bronze_badges(self):

        if hasattr(self, 'count_bronze_badges'):
            return self.count_bronze_badges

        return self.get_bronze_badges().count()
    get_count_bronze_badges.short_description = _('Count bronze badges')
    get_count_bronze_badges.admin_order_field = 'count_bronze_badges'

    def get_latest_badge(self):

        if hasattr(self, 'pk_latest_badge'):
            if self.pk_latest_badge is not None:
                return Badge._default_manager.get(pk=self.pk_latest_badge)
            return

        try:
            return self.badges.latest().badge
        except self.badges.model.DoesNotExist:
            return
    get_latest_badge.short_description = _('Latest badge')
    # get_latest_badge.admin_order_field = 'badges__badge__name'

    def get_date_getting_latest_badge(self):

        if hasattr(self, 'date_latest_badge'):
            return self.date_latest_badge

        try:
            return self.badges.latest().created
        except self.badges.model.DoesNotExist:
            return
    get_date_getting_latest_badge.short_description = _('Date getting latest badge')
    get_date_getting_latest_badge.admin_order_field = 'date_latest_badge'

    def get_earned_badges(self):

        return self.badges.all()

    def get_unearned_badges(self):

        return Badge._default_manager.exclude(pk__in=self.badges.all())

    def get_gold_badges(self):

        return self.badges.filter(badge__kind=Badges.Kind.GOLD.value)

    def get_silver_badges(self):

        return self.badges.filter(badge__kind=Badges.Kind.SILVER.value)

    def get_bronze_badges(self):

        return self.badges.filter(badge__kind=Badges.Kind.BRONZE.value)
