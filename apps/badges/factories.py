
import factory

from .models import *


class BadgeFactory(factory.DjangoModelFactory):

    class Meta:
        model = Badge


def badges_factory():
    Badge.objects.filter().delete()
    # Badge for questions/answers
    BadgeFactory(name='Favorite question', short_description='Question favorited by 5 users')
    BadgeFactory(name='Stellar question', short_description='Question favorited by 10 users')
    BadgeFactory(name='Nice Question', short_description='Question score of 5 or more')
    BadgeFactory(name='Good Question', short_description='Question score of 10 or more')
    BadgeFactory(name='Great Question', short_description='Question score of 20 or more')
    BadgeFactory(name='Popular Question', short_description='Question with 100 views')
    BadgeFactory(name='Notable Question', short_description='Question with 500 views')
    BadgeFactory(name='Famous Question', short_description='Question with 1000 views')
    BadgeFactory(name='Schoolar', short_description='Ask a question and acceped an answer')
    BadgeFactory(name='Student', short_description='Accepted an answer on 5 questions')
    BadgeFactory(name='Tumbleweed', short_description='Asked a question with zero score or less, no answers.')
    BadgeFactory(name='Enlightened', short_description='Have accepted answer with score of 10 or more')
    BadgeFactory(name='Explainer', short_description='Answer on 1 question within 24 hours and with scope > 0')
    BadgeFactory(name='Refiner', short_description='Answer on 5 questions within 24 hours with scope > 0')
    BadgeFactory(name='Illuminator', short_description='Answer on 10 question within 24 hours with scope > 0')
    BadgeFactory(name='Guru', short_description='Given accepted answer with score of 5 or more.')
    BadgeFactory(name='Teacher', short_description='Answer a question with score of 1 or more')
    BadgeFactory(name='Nice answer', short_description='Answer score of 5 or more')
    BadgeFactory(name='Good answer', short_description='Answer score of 10 or more')
    BadgeFactory(name='Great answer', short_description='Answer score of 15 or more')
    BadgeFactory(name='Populist', short_description='Highest scoring answer that outscored an accepted answer')
    BadgeFactory(name='Reversal', short_description='Provide an answer of +1 score to a question of -1 score')
    BadgeFactory(name='Revival', short_description='Answer more than 7 days after a question was asked')
    BadgeFactory(name='Necromancer', short_description='Answer a question more than 60 days later with score of 5 or more')
    BadgeFactory(name='Self-learner', short_description='Answer your own question with score of 1 or more.')
    BadgeFactory(name='Supporter', short_description='Have answer and question with scope +3 and more.')
    # Other
    BadgeFactory(name='Autobiograther', short_description='Completed fill up account profile.')
    BadgeFactory(name='Commentator', short_description='Leave 10 comments')
    BadgeFactory(name='Sociable', short_description='Leave 20 comments')
    BadgeFactory(name='Enthusiast', short_description='Visit the site each day for 5 consecutive days')
    BadgeFactory(name='Fanatic', short_description='Visit the site each day for 10 consecutive days')
    # Reputation
    BadgeFactory(name='Eager', short_description='Earn reputation 100 and more')
    BadgeFactory(name='Epic', short_description='Earn reputation 1000 and more')
    BadgeFactory(name='Legendary', short_description='Earn reputation 10000 and more')
    # Forum
    BadgeFactory(name='Citizen', short_description='Have more than 1 post on forum.')
    BadgeFactory(name='Talkative', short_description='Have more than 10 post on forum')
    BadgeFactory(name='Outspoken', short_description='Have more than 15 post on forum')
    BadgeFactory(name='Yearning', short_description='Active member for a year, earning at least 200 reputation')
    BadgeFactory(name='Civic Duty', short_description='Given 10 opinions or more times')
    BadgeFactory(name='Electorate', short_description='Given 15 opinions  or more times')
    BadgeFactory(name='Citizen Patrol', short_description='Have 5 and more favorited objects.')
    BadgeFactory(name='Depute', short_description='Have 10 and more favorited objects.')
    BadgeFactory(name='Marshal', short_description='Have 15 and more favorited objects')
    BadgeFactory(name='Critic', short_description='Have answer with scope -3 and less.')
    BadgeFactory(name='Nonsense', short_description='Have question with scope -3 and less.')
    BadgeFactory(name='Publicist', short_description='Publicated own article')
    BadgeFactory(name='Tester', short_description='Passed at leat 1 testsuit')
    BadgeFactory(name='Creator tests', short_description='Create own testing suit.')
    BadgeFactory(name='Clear mind', short_description='Added own solution with scope +1 or more.')
    BadgeFactory(name='Clear head', short_description='Added own snippet with scope +1 or more.')
    BadgeFactory(name='Dispatcher', short_description='Used links in own articles or solutions.')
    BadgeFactory(name='Sage', short_description='Participated in creating courses')
    BadgeFactory(name='Voter', short_description='Voted in polls')
    # BadgeFactory(name='Closer questions', short_description='Closed questions')
    # BadgeFactory(name='Deleter questions', short_description='Deleted questions')
    # BadgeFactory(name='Editor', short_description='First edit')
    # BadgeFactory(name='Organizer', short_description='Added new tag')
    # BadgeFactory(name='Suffrage', short_description='Use 10 votes in day')
    # BadgeFactory(name='Vox populi', short_description='Use 30 votes in day')
    # BadgeFactory(name='Taxonomist', short_description='Created tag used by 50 times')
