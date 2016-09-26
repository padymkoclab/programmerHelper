
# from .managers import BadgeManager
#
from .models import Badge


BADGES = (

    # Comments
    {
        'name': 'Commentator',
        'description': 'Has 10 comments',
        'kind': Badge.BRONZE,
        'category': Badge.COMMENTS,
    },
    {
        'name': 'Pundit',
        'description': 'Has 10 comments with rating more 10',
        'kind': Badge.SILVER,
        'category': Badge.COMMENTS,
    },

    # Polls
    {
        'name': 'Voter',
        'description': 'Has vote in poll',
        'kind': Badge.BRONZE,
        'category': Badge.POLLS,
    },
    {
        'name': 'Electorate',
        'description': 'Has vote in more than half count of all polls',
        'kind': Badge.SILVER,
        'category': Badge.POLLS,
    },
    {
        'name': 'Vox Populi',
        'description': 'Has vote in all polls',
        'kind': Badge.GOLD,
        'category': Badge.POLLS,
    },

    # Articles
    {
        'name': 'Good publicist',
        'description': 'Has article with rating more 0',
        'kind': Badge.BRONZE,
        'category': Badge.ARTICLES,
    },
    {
        'name': 'Big publicist',
        'description': 'Has article with rating more 10',
        'kind': Badge.SILVER,
        'category': Badge.ARTICLES,
    },
    {
        'name': 'Great publicist',
        'description': 'Has article with rating more 50',
        'kind': Badge.GOLD,
        'category': Badge.ARTICLES,
    },
    {
        'name': 'Popular article',
        'description': 'Article with 100 views',
        'kind': Badge.BRONZE,
        'category': Badge.ARTICLES,
    },

    # Snippets
    {
        'name': 'Good coder',
        'description': 'Has snippet with rating more 0',
        'kind': Badge.BRONZE,
        'category': Badge.SNIPPETS,
    },
    {
        'name': 'Big coder',
        'description': 'Has snippet with rating more 10',
        'kind': Badge.SILVER,
        'category': Badge.SNIPPETS,
    },
    {
        'name': 'Great coder',
        'description': 'Has snippet with rating more 50',
        'kind': Badge.GOLD,
        'category': Badge.SNIPPETS,
    },
    {
        'name': 'Popular snippet',
        'description': 'Snippet with 100 views',
        'kind': Badge.BRONZE,
        'category': Badge.SNIPPETS,
    },

    # Solutions
    {
        'name': 'Good inventor',
        'description': 'Has solutions with rating more 0',
        'kind': Badge.BRONZE,
        'category': Badge.SOLUTIONS,
    },
    {
        'name': 'Big inventor',
        'description': 'Has solutions with rating more 0',
        'kind': Badge.SILVER,
        'category': Badge.SOLUTIONS,
    },
    {
        'name': 'Great inventor',
        'description': 'Has solutions with rating more 0',
        'kind': Badge.GOLD,
        'category': Badge.SOLUTIONS,
    },
    {
        'name': 'Popular solution',
        'description': 'Solution with 100 views',
        'kind': Badge.BRONZE,
        'category': Badge.SOLUTIONS,
    },

    # Questions
    {
        'name': 'Popular question',
        'description': 'Question with 100 views',
        'kind': Badge.BRONZE,
        'category': Badge.QUESTIONS,
    },
    {
        'name': 'Good question',
        'description': 'Has question with rating more 0',
        'kind': Badge.BRONZE,
        'category': Badge.QUESTIONS,
    },
    {
        'name': 'Big question',
        'description': 'Has question with rating more 10',
        'kind': Badge.SILVER,
        'category': Badge.QUESTIONS,
    },
    {
        'name': 'Great question',
        'description': 'Has question with rating more 50',
        'kind': Badge.GOLD,
        'category': Badge.QUESTIONS,
    },


    {
        'name': 'Teacher',
        'description': 'Has answer with ration more 0',
        'kind': Badge.BRONZE,
        'category': Badge.ANSWERS,
    },
    {
        'name': 'Enlightened',
        'description': 'Has answer with rating more 10',
        'kind': Badge.SILVER,
        'category': Badge.ANSWERS,
    },
    {
        'name': 'Guru',
        'description': 'Has answer with rating more 50',
        'kind': Badge.GOLD,
        'category': Badge.ANSWERS,
    },
    {
        'name': 'Self-Learner',
        'description': 'Answer your own question with rating of 3 or more',
        'kind': Badge.BRONZE,
        'category': Badge.ANSWERS,
    },
    {
        'name': 'Schoolar',
        'description': 'Ask a question and accept an answer',
        'kind': Badge.BRONZE,
        'category': Badge.ANSWERS,
    },

    # Forums
    {
        'name': 'Interlocutor',
        'description': 'Has post on forum',
        'kind': Badge.BRONZE,
        'category': Badge.FORUMS,
    },
    {
        'name': 'Initializer of conversation',
        'description': 'Has topic on forum',
        'kind': Badge.BRONZE,
        'category': Badge.FORUMS,
    },

    # Other
    {
        'name': 'Enthusiast',
        'description': 'Visit the site each day for 30 consecutive days.',
        'kind': Badge.BRONZE,
        'category': Badge.OTHER,
    },
    {
        'name': 'Editor',
        'description': 'First edit',
        'kind': Badge.BRONZE,
        'category': Badge.OTHER,
    },
    {
        'name': 'Frequent recorder',
        'description': 'Has at least 250000 characters in a diary',
        'kind': Badge.BRONZE,
        'category': Badge.OTHER,
    },
    {
        'name': 'Fanatic',
        'description': 'Visit the site each day for 100 consecutive days.',
        'kind': Badge.SILVER,
        'category': Badge.OTHER,
    },
    {
        'name': 'Epic',
        'description': 'Reputation is more than 1000',
        'kind': Badge.SILVER,
        'category': Badge.OTHER,
    },
    {
        'name': 'Legendary',
        'description': 'Reputation is more than 10000',
        'kind': Badge.GOLD,
        'category': Badge.OTHER,
    },
    {
        'name': 'Yearling',
        'description': 'More 1 year as registered',
        'kind': Badge.BRONZE,
        'category': Badge.OTHER,
    },

    # Profile
    {
        'name': 'Autobiographer',
        'description': 'Filled profile on more or equal 90%',
        'kind': Badge.BRONZE,
        'category': Badge.PROFILE,
    },

    # Opinions
    {
        'name': 'Critic',
        'description': 'First down vote',
        'kind': Badge.BRONZE,
        'category': Badge.PROFILE,
    },
    {
        'name': 'Supporter',
        'description': 'First up vote',
        'kind': Badge.BRONZE,
        'category': Badge.PROFILE,
    },

    # Testing
    {
        'name': 'Tester',
        'description': 'Has more 10 passages of tests',
        'kind': Badge.BRONZE,
        'category': Badge.TESTING,
    },
    {
        'name': 'Love tests',
        'description': 'Has more 100 passages of tests',
        'kind': Badge.SILVER,
        'category': Badge.TESTING,
    },

    # Flavors
    {
        'name': 'Popularic flavour',
        'description': 'Has snippet or article or solutions or question favorited more 25 users',
        'kind': Badge.BRONZE,
        'category': Badge.FLAVOURS,
    },
    {
        'name': 'Famous flavour',
        'description': 'Has snippet or article or solutions or question favorited more 50 users',
        'kind': Badge.SILVER,
        'category': Badge.FLAVOURS,
    },

    # Marks
    {
        'name': 'Made an assessment',
        'description': 'Give mark',
        'kind': Badge.BRONZE,
        'category': Badge.MARKS,
    },

    # Replies
    {
        'name': 'Reading',
        'description': 'Has reply about any book',
        'kind': Badge.BRONZE,
        'category': Badge.REPLIES,
    },
    {
        'name': 'More reading',
        'description': 'Has more 10 replies about books',
        'kind': Badge.SILVER,
        'category': Badge.REPLIES,
    },

    # Planning
    # ('Talkative', 'Has 100 messages in a chat'),
    # ('Outspoken', 'Has 1000 messages in a chat'),
)
