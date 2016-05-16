
import factory

from .models import *


class Factory_Badges(factory.DjangoModelFactory):

    class Meta:
        model = Badge


Badge.objects.filter().delete()

# Badge for questions/answers
# Factory_Badges(name='Favorite question', short_description='Question favorited by 5 users')
# Factory_Badges(name='Stellar question', short_description='Question favorited by 10 users')
# Factory_Badges(name='Nice Question', short_description='Question score of 5 or more')
# Factory_Badges(name='Good Question', short_description='Question score of 10 or more')
# Factory_Badges(name='Great Question', short_description='Question score of 20 or more')
# Factory_Badges(name='Popular Question', short_description='Question with 100 views')
# Factory_Badges(name='Notable Question', short_description='Question with 500 views')
# Factory_Badges(name='Famous Question', short_description='Question with 1000 views')
# Factory_Badges(name='Schoolar', short_description='Ask a question and acceped an answer')
# Factory_Badges(name='Student', short_description='Accepted an answer on 5 questions')
# Factory_Badges(name='Tumbleweed', short_description='Asked a question with zero score or less, no answers.')
# Factory_Badges(name='Enlightened', short_description='Have accepted answer with score of 10 or more')
# Factory_Badges(name='Explainer', short_description='Answer on 1 question within 24 hours and with scope > 0')
# Factory_Badges(name='Refiner', short_description='Answer on 5 questions within 24 hours with scope > 0')
# Factory_Badges(name='Illuminator', short_description='Answer on 10 question within 24 hours with scope > 0')
# Factory_Badges(name='Guru', short_description='Given accepted answer with score of 5 or more.')
# Factory_Badges(name='Teacher', short_description='Answer a question with score of 1 or more')
# Factory_Badges(name='Nice answer', short_description='Answer score of 5 or more')
# Factory_Badges(name='Good answer', short_description='Answer score of 10 or more')
# Factory_Badges(name='Great answer', short_description='Answer score of 15 or more')
# Factory_Badges(name='Populist', short_description='Highest scoring answer that outscored an accepted answer')
# Factory_Badges(name='Reversal', short_description='Provide an answer of +1 score to a question of -1 score')
# Factory_Badges(name='Revival', short_description='Answer more than 7 days after a question was asked')
# Factory_Badges(name='Necromancer', short_description='Answer a question more than 60 days later with score of 5 or more')
# Factory_Badges(name='Self-learner', short_description='Answer your own question with score of 1 or more.')
# Factory_Badges(name='Supporter', short_description='Have answer and question with scope +3 and more.')
# Other
# Factory_Badges(name='Autobiograther', short_description='Completed fill up account profile.')
# Factory_Badges(name='Commentator', short_description='Leave 10 comments')
# Factory_Badges(name='Sociable', short_description='Leave 20 comments')
Factory_Badges(name='Enthusiast', short_description='Visit the site each day for 5 consecutive days')
Factory_Badges(name='Fanatic', short_description='Visit the site each day for 10 consecutive days')
# Reputation
# Factory_Badges(name='Eager', short_description='Earn reputation 100 and more')
# Factory_Badges(name='Epic', short_description='Earn reputation 1000 and more')
# Factory_Badges(name='Legendary', short_description='Earn reputation 10000 and more')
# Forum
# Factory_Badges(name='Citizen', short_description='Have more than 1 post on forum.')
# Factory_Badges(name='Talkative', short_description='Have more than 10 post on forum')
# Factory_Badges(name='Outspoken', short_description='Have more than 15 post on forum')
# Factory_Badges(name='Yearning', short_description='Active member for a year, earning at least 200 reputation')
# Factory_Badges(name='Civic Duty', short_description='Given 10 opinions or more times')
# Factory_Badges(name='Electorate', short_description='Given 15 opinions  or more times')
# Factory_Badges(name='Citizen Patrol', short_description='Have 5 and more favorited objects.')
# Factory_Badges(name='Depute', short_description='Have 10 and more favorited objects.')
# Factory_Badges(name='Marshal', short_description='Have 15 and more favorited objects')
# Factory_Badges(name='Critic', short_description='Have answer with scope -3 and less.')
# Factory_Badges(name='Nonsense', short_description='Have question with scope -3 and less.')
Factory_Badges(name='Editor', short_description='First edit')
Factory_Badges(name='Organizer', short_description='Added new tag')
Factory_Badges(name='Suffrage', short_description='Use 10 votes in day')
Factory_Badges(name='Vox populi', short_description='Use 30 votes in day')
Factory_Badges(name='Taxonomist', short_description='Created tag used by 50 times')
# Factory_Badges(name='Publicist', short_description='Publicated own article')
# Factory_Badges(name='Tester', short_description='Passed at leat 1 testsuit')
# Factory_Badges(name='Creator tests', short_description='Create own testing suit.')
# Factory_Badges(name='Clear mind', short_description='Added own solution with scope +1 or more.')
# Factory_Badges(name='Clear head', short_description='Added own snippet with scope +1 or more.')
Factory_Badges(name='Closer questions', short_description='Closed questions')
Factory_Badges(name='Deleter questions', short_description='Deleted questions')
# Factory_Badges(name='Dispatcher', short_description='Used links in own articles or solutions.')
# Factory_Badges(name='Sage', short_description='Participated in creating courses')
# Factory_Badges(name='Voter', short_description='Voted in polls')
