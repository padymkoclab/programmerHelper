
from django.utils.translation import ugettext_lazy as _


class UserPollModelMixin(object):
    """

    """

    def get_count_votes(self):
        """ """

        if hasattr(self, 'count_votes'):
            return self.count_votes

        return self.votes.count()
    get_count_votes.admin_order_field = 'count_votes'
    get_count_votes.short_description = _('Count votes')

    def get_date_latest_vote(self):
        """ """

        try:
            return self.votes.latest().created
        except self.votes.model.DoesNotExist:
            return
    get_date_latest_vote.admin_order_field = 'date_latest_voting'
    get_date_latest_vote.short_description = _('Date latest voting')

    def is_active_voter(self):
        """ """

        from .model import Poll

        count_polls = Poll._default_manager.count()

        half_count_polls = count_polls / 2

        return self.get_count_votes() > half_count_polls
    is_active_voter.admin_order_field = 'is_active_voter'
    is_active_voter.short_description = _('Is active voter?')
    is_active_voter.boolean = True
