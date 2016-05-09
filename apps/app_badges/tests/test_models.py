
from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from .models import *


class Factory_Badges(factory.DjangoModelFactory):

    class Meta:
        model = Badge


Factory_Badges(name='Favorite question', short_description='Question favorited by 25 users')
Factory_Badges(name='Stellar question', short_description='Question favorited by 100 users')
Factory_Badges(name='Nice Question', short_description='Question score of 10 or more')
Factory_Badges(name='Good Question', short_description='Question score of 25 or more')
Factory_Badges(name='Great Question', short_description='Question score of 100 or more')
Factory_Badges(name='Popular Question', short_description='Question with 1,000 views')
Factory_Badges(name='Notable Question', short_description='Question with 2,500 views')
Factory_Badges(name='Famous Question', short_description='Question with 10,000 views')
Factory_Badges(name='Schoolar', short_description='Ask a question and accept an answer')
Factory_Badges(name='Student', short_description='First question with score of 1 or more')
Factory_Badges(name='Tumbleweed', short_description='Asked a question with zero score, no answers, no comments')
Factory_Badges(name='Enlightened', short_description='First to answer and accepted with score of 10 or more')
Factory_Badges(name='Explainer', short_description='Answer on 1 question with scope > 0 within 12 hours')
Factory_Badges(name='Refiner', short_description='Answer on 50 questions with scope > 0 within 12 hours')
Factory_Badges(name='Illuminator', short_description='Answer on 500 question with scope > 0 within 12 hours')
Factory_Badges(name='Guru', short_description='Accepted answer and score of 40 or more')
Factory_Badges(name='Nice answer', short_description='Answer score of 10 or more')
Factory_Badges(name='Good answer', short_description='Answer score of 25 or more')
Factory_Badges(name='Great answer', short_description='Answer score of 100 or more')
Factory_Badges(name='Populist', short_description='Highest scoring answer that outscored an accepted answer')
Factory_Badges(name='Reversal', short_description='Provide an answer of +20 score to a question of -5 score')
Factory_Badges(name='Revival', short_description='Answer more than 30 days after a question was asked')
Factory_Badges(name='Necromancer', short_description='Answer a question more than 60 days later with score of 5 or more')
Factory_Badges(name='Self-learner', short_description='Answer your own question with score of 3 or more')
Factory_Badges(name='Teacher', short_description='Answer a question with score of 1 or more')
Factory_Badges(name='Autobiograther', short_description='Complete fill up account profile')
Factory_Badges(name='Commentator', short_description='Leave 10 comments')
Factory_Badges(name='Sociable', short_description='Leave 100 comments')
Factory_Badges(name='Enthusiast', short_description='Visit the site each day for 30 consecutive days')
Factory_Badges(name='Fanatic', short_description='Visit the site each day for 100 consecutive days')
Factory_Badges(name='Assduous', short_description='Earn reputation 100')
Factory_Badges(name='Epic', short_description='Earn reputation 1000')
Factory_Badges(name='Legendary', short_description='Earn reputation 10000')
Factory_Badges(name='Citize', short_description='1 post on forum')
Factory_Badges(name='Talkative', short_description='10 post on forum')
Factory_Badges(name='Outspoken', short_description='100 post on forum')
Factory_Badges(name='Yearning', short_description='Active member for a year, earning at least 200 reputation')
Factory_Badges(name='Civic Duty', short_description='Vote 300 or more times')
Factory_Badges(name='Electorate', short_description='Vote 600 or more times')
Factory_Badges(name='Citizen Patrol', short_description='Have 1 favorited element')
Factory_Badges(name='Depute', short_description='Have 10 favorited elements')
Factory_Badges(name='Marshal', short_description='Have 100 favorited elements')
Factory_Badges(name='Critic', short_description='Had 1 down vote')
Factory_Badges(name='Editor', short_description='First edit')
Factory_Badges(name='Organizer', short_description='Added new tag')
Factory_Badges(name='Proofreader', short_description='Approve or reject 100 suggested edits')
Factory_Badges(name='Suffrage', short_description='Use 10 votes in day')
Factory_Badges(name='Vox populi', short_description='Use 30 votes in day')
Factory_Badges(name='Supporter', short_description='Had 1 up vote')
Factory_Badges(name='Taxonomist', short_description='Created tag used by 50 times')
Factory_Badges(name='Publicist', short_description='Publicated own article')
Factory_Badges(name='Tester', short_description='Passed at leat 1 testsuit')
Factory_Badges(name='Creator tests', short_description='Create own testsuit')
Factory_Badges(name='Clear mind', short_description='Added own solution')
Factory_Badges(name='Clear head', short_description='Added own snippet')
Factory_Badges(name='Closer questions', short_description='Closed questions')
Factory_Badges(name='Deleter questions', short_description='Deleted questions')
Factory_Badges(name='Dispatcher', short_description='Used links in own articles or solutions')
Factory_Badges(name='Sage', short_description='Participating in creating courses')
Factory_Badges(name='Have opinion', short_description='Voted in polls')


class Factory_GettingBadgeUser(factory.DjangoModelFactory):

    class Meta:
        model = GettingBadgeUser

    user = fuzzy.FuzzyChoice(get_user_model().objects.filter(is_active=True).all())
    badge = fuzzy.FuzzyChoice(Badge.objects.all())
