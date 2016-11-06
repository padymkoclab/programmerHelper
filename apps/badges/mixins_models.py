
from django.utils.translation import ugettext_lazy as _

from .constants import Badges


class BadgeModelMixin(object):
    """

    """

    def has_badge(self, badge):

        return self.badges.filter(badge=badge).exists()

    def get_count_badges(self):

        return self.badges.count()
    get_count_badges.short_description = _('Count badges')
    get_count_badges.admin_order_field = 'count_badges'

    def get_count_gold_badges(self):

        return self.get_gold_badges().count()
    get_count_gold_badges.short_description = _('Count gold badges')
    get_count_gold_badges.admin_order_field = 'count_gold_badges'

    def get_count_silver_badges(self):

        return self.get_silver_badges().count()
    get_count_silver_badges.short_description = _('Count silver badges')
    get_count_silver_badges.admin_order_field = 'count_silver_badges'

    def get_count_bronze_badges(self):

        return self.get_bronze_badges().count()
    get_count_bronze_badges.short_description = _('Count bronze badges')
    get_count_bronze_badges.admin_order_field = 'count_bronze_badges'

    def get_latest_badge(self):

        try:
            return self.badges.latest()
        except self.badges.model.DoesNotExist:
            return
    get_latest_badge.short_description = _('Latest badge')
    get_latest_badge.admin_order_field = 'latest_badge'

    def get_date_getting_latest_badge(self):

        try:
            return self.badges.latest().date
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
