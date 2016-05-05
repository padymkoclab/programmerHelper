
# from django.contrib.auth import get_user_model
from django.db import models


class BadgeManager(models.Manager):
    """
    Model manager for working with badges of account
    """

    def analysis_badges_account(self, account):
        account.badges.all()

    def get_latest_users_obtained_badges(self):
        pass
        # return self.accounts.ord

    def function(self):
        pass

"""
(name='Favorite question', short_description='Question favorited by 25 users')
(name='Stellar question', short_description='Question favorited by 100 users')
(name='Nice Question', short_description='Question score of 10 or more')
(name='Good Question', short_description='Question score of 25 or more')
(name='Great Question', short_description='Question score of 100 or more')
(name='Popular Question', short_description='Question with 1,000 views')
(name='Notable Question', short_description='Question with 2,500 views')
(name='Famous Question', short_description='Question with 10,000 views')
(name='Schoolar', short_description='Ask a question and accept an answer')
(name='Student', short_description='First question with score of 1 or more')
(name='Tumbleweed', short_description='Asked a question with zero score, no answers, no comments')
(name='Enlightened', short_description='First to answer and accepted with score of 10 or more')
(name='Explainer', short_description='Answer on 1 question with scope > 0 within 12 hours')
(name='Refiner', short_description='Answer on 50 questions with scope > 0 within 12 hours')
(name='Illuminator', short_description='Answer on 500 question with scope > 0 within 12 hours')
(name='Guru', short_description='Accepted answer and score of 40 or more')
(name='Nice answer', short_description='Answer score of 10 or more')
(name='Good answer', short_description='Answer score of 25 or more')
(name='Great answer', short_description='Answer score of 100 or more')
(name='Populist', short_description='Highest scoring answer that outscored an accepted answer')
(name='Reversal', short_description='Provide an answer of +20 score to a question of -5 score')
(name='Revival', short_description='Answer more than 30 days after a question was asked')
(name='Necromancer', short_description='Answer a question more than 60 days later with score of 5 or more')
(name='Self-learner', short_description='Answer your own question with score of 3 or more')
(name='Teacher', short_description='Answer a question with score of 1 or more')
(name='Autobiograther', short_description='Complete fill up account profile')
(name='Commentator', short_description='Leave 10 comments')
(name='Sociable', short_description='Leave 100 comments')
(name='Enthusiast', short_description='Visit the site each day for 30 consecutive days')
(name='Fanatic', short_description='Visit the site each day for 100 consecutive days')
(name='Assduous', short_description='Earn reputation 100')
(name='Epic', short_description='Earn reputation 1000')
(name='Legendary', short_description='Earn reputation 10000')
(name='Citize', short_description='1 post on forum')
(name='Talkative', short_description='10 post on forum')
(name='Outspoken', short_description='100 post on forum')
(name='Yearning', short_description='Active member for a year, earning at least 200 reputation')
(name='Civic Duty', short_description='Vote 300 or more times')
(name='Electorate', short_description='Vote 600 or more times')
(name='Citizen Patrol', short_description='Have 1 favorited element')
(name='Depute', short_description='Have 10 favorited elements')
(name='Marshal', short_description='Have 100 favorited elements')
(name='Critic', short_description='Had 1 down vote')
(name='Editor', short_description='First edit')
(name='Organizer', short_description='Added new tag')
(name='Proofreader', short_description='Approve or reject 100 suggested edits')
(name='Suffrage', short_description='Use 10 votes in day')
(name='Vox populi', short_description='Use 30 votes in day')
(name='Supporter', short_description='Had 1 up vote')
(name='Taxonomist', short_description='Created tag used by 50 times')
(name='Publicist', short_description='Publicated own article')
(name='Tester', short_description='Passed at leat 1 testsuit')
(name='Creator tests', short_description='Create own testsuit')
(name='Clear mind', short_description='Added own solution')
(name='Clear head', short_description='Added own snippet')
(name='Closer questions', short_description='Closed questions')
(name='Deleter questions', short_description='Deleted questions')
(name='Dispatcher', short_description='Used links in own articles or solutions')
(name='Sage', short_description='Participate in creating courses')
(name='Have opinion', short_description='Voted in polls')
"""
