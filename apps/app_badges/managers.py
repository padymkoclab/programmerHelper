
from django.contrib.auth import get_user_model
from django.db import models


class BadgeManager(models.Manager):
    """
    Model manager for working with badges of account
    """

    def validate_badges(self, account_natural_key):
        account = get_user_model().objects.get_by_natural_key(account_natural_key)
        self.check_badge_Favorite_Question(account)
        # return account

    # def has_badge(self, account, badge):
    #     try:
    #         GettingBadge.objects.get(account=account, badge=badge)
    #     except GettingBadge.DoesNotExist:
    #         return False
    #     else:
    #         return True

    # def last_got_badges(self, count=10):
    #     return GettingBadge.objects.order_by('-date_getting')[:count]

    def check_badge_Favorite_Question(self, account):
        for account in self.iterator():
            pass

        # Favorite question
        # Stellar question
        # Nice Question
        # Good Question
        # Great Question
        # Popular Question
        # Notable Question
        # Famous Question
        # Schoolar
        # Student
        # Tumbleweed
        # Enlightened
        # Explainer
        # Refiner
        # Illuminator
        # Guru
        # Nice answer
        # Good answer
        # Great answer
        # Populist
        # Reversal
        # Revival
        # Necromancer
        # Self-learner
        # Teacher
        # Autobiograther
        # Commentator
        # Sociable
        # Enthusiast
        # Fanatic
        # Assduous
        # Epic
        # Legendary
        # Citize
        # Talkative
        # Outspoken
        # Yearning
        # Civic Duty
        # Electorate
        # Citizen Patrol
        # Depute
        # Marshal
        # Critic
        # Editor
        # Organizer
        # Proofreader
        # Suffrage
        # Vox populi
        # Supporter
        # Taxonomist
        # Publicist
        # Tester
        # Creator tests
        # Clear mind
        # Clear head
        # Closer questions
        # Deleter questions
        # Dispatcher
        # Sage
        # Have opinion
