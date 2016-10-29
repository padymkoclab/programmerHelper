
import enum

from django.utils.translation import ugettext_lazy as _

from utils.python.utils import classproperty

from . import behaviors


class Badges(object):
    """

    """

    @enum.unique
    class Category(enum.Enum):

        ANSWERS = 'answers'
        ARTICLES = 'articles'
        CHAT = 'chat'
        COMMENTS = 'comments'
        FORUMS = 'forums'
        LIBRARY = 'library'
        OPINIONS = 'opinions'
        OTHER = 'other'
        POLLS = 'polls'
        PROFILE = 'profile'
        QUESTIONS = 'questions'
        SNIPPETS = 'snippets'
        SOLUTIONS = 'solutions'

    @enum.unique
    class Badge(enum.Enum):

        AUTOBIOGRAPHER_BRONZE = 'autobiographer_bronze'
        BIBLIOPHILE_GOLD = 'bibliophile_gold'
        BOOKLOVER_SILVER = 'booklover_silver'
        CODER_BRONZE = 'coder_bronze'
        CODER_GOLD = 'coder_gold'
        CODER_SILVER = 'coder_silver'
        COMMENTATOR_BRONZE = 'commentator_bronze'
        COMMENTATOR_GOLD = 'commentator_gold'
        COMMENTATOR_SILVER = 'commentator_silver'
        CRITIC_BRONZE = 'critic_bronze'
        ENLIGHTENED_SILVER = 'enlightened_silver'
        ENTHUSIAST_BRONZE = 'enthusiast_bronze'
        EPIC_SILVER = 'epic_silver'
        FANATIC_SILVER = 'fanatic_silver'
        FORUMER_SILVER = 'forumer_silver'
        FREQUENT_RECORDER_BRONZE = 'frequent_recorder_bronze'
        GURU_GOLD = 'guru_gold'
        INITIALIZER_CONVERSATION_BRONZE = 'initializer_conversation_bronze'
        INTERLOCUTOR_BRONZE = 'interlocutor_bronze'
        INVENTOR_BRONZE = 'inventor_bronze'
        INVENTOR_GOLD = 'inventor_gold'
        INVENTOR_SILVER = 'inventor_silver'
        LEGENDARY_GOLD = 'legendary_gold'
        OUTSPOKEN_BRONZE = 'outspoken_bronze'
        PUBLICIST_BRONZE = 'publicist_bronze'
        PUBLICIST_GOLD = 'publicist_gold'
        PUBLICIST_SILVER = 'publicist_silver'
        QUESTIONER_BRONZE = 'questioner_bronze'
        QUESTIONER_GOLD = 'questioner_gold'
        QUESTIONER_SILVER = 'questioner_silver'
        READER_BRONZE = 'reader_bronze'
        SCHOOLAR_BRONZE = 'schoolar_bronze'
        SELF_LEARNER_BRONZE = 'self_learner_bronze'
        SUPPORTER_BRONZE = 'supporter_bronze'
        TALKATIVE_BRONZE = 'talkative_bronze'
        TEACHER_BRONZE = 'teacher_bronze'
        VOTER_BRONZE = 'voter_bronze'
        VOTER_GOLD = 'voter_gold'
        VOTER_SILVER = 'voter_silver'
        YEARLING_BRONZE = 'yearling_bronze'

    @enum.unique
    class Kind(enum.Enum):

        BRONZE = 'bronze'
        GOLD = 'gold'
        SILVER = 'silver'

    @classproperty
    def checkers(cls):

        return {
            cls.Badge.AUTOBIOGRAPHER_BRONZE: behaviors.check_badge_autobiographer_bronze,
            cls.Badge.BIBLIOPHILE_GOLD: behaviors.check_badge_bibliophile_gold,
            cls.Badge.BOOKLOVER_SILVER: behaviors.check_badge_booklover_silver,
            cls.Badge.CODER_BRONZE: behaviors.check_badge_coder_bronze,
            cls.Badge.CODER_GOLD: behaviors.check_badge_coder_gold,
            cls.Badge.CODER_SILVER: behaviors.check_badge_coder_silver,
            cls.Badge.COMMENTATOR_BRONZE: behaviors.check_badge_commentator_bronze,
            cls.Badge.COMMENTATOR_GOLD: behaviors.check_badge_commentator_gold,
            cls.Badge.COMMENTATOR_SILVER: behaviors.check_badge_commentator_silver,
            cls.Badge.CRITIC_BRONZE: behaviors.check_badge_critic_bronze,
            cls.Badge.ENLIGHTENED_SILVER: behaviors.check_badge_enlightened_silver,
            cls.Badge.ENTHUSIAST_BRONZE: behaviors.check_badge_enthusiast_bronze,
            cls.Badge.EPIC_SILVER: behaviors.check_badge_epic_silver,
            cls.Badge.FANATIC_SILVER: behaviors.check_badge_fanatic_silver,
            cls.Badge.FORUMER_SILVER: behaviors.check_badge_forumer_silver,
            cls.Badge.FREQUENT_RECORDER_BRONZE: behaviors.check_badge_frequent_recorder_bronze,
            cls.Badge.GURU_GOLD: behaviors.check_badge_guru_gold,
            cls.Badge.INITIALIZER_CONVERSATION_BRONZE: behaviors.check_badge_initializer_conversation_bronze,
            cls.Badge.INTERLOCUTOR_BRONZE: behaviors.check_badge_interlocutor_bronze,
            cls.Badge.INVENTOR_BRONZE: behaviors.check_badge_inventor_bronze,
            cls.Badge.INVENTOR_GOLD: behaviors.check_badge_inventor_gold,
            cls.Badge.INVENTOR_SILVER: behaviors.check_badge_inventor_silver,
            cls.Badge.LEGENDARY_GOLD: behaviors.check_badge_legendary_gold,
            cls.Badge.OUTSPOKEN_BRONZE: behaviors.check_badge_outspoken_bronze,
            cls.Badge.PUBLICIST_BRONZE: behaviors.check_badge_publicist_bronze,
            cls.Badge.PUBLICIST_GOLD: behaviors.check_badge_publicist_gold,
            cls.Badge.PUBLICIST_SILVER: behaviors.check_badge_publicist_silver,
            cls.Badge.QUESTIONER_BRONZE: behaviors.check_badge_questioner_bronze,
            cls.Badge.QUESTIONER_GOLD: behaviors.check_badge_questioner_gold,
            cls.Badge.QUESTIONER_SILVER: behaviors.check_badge_questioner_silver,
            cls.Badge.READER_BRONZE: behaviors.check_badge_reader_bronze,
            cls.Badge.SCHOOLAR_BRONZE: behaviors.check_badge_schoolar_bronze,
            cls.Badge.SELF_LEARNER_BRONZE: behaviors.check_badge_self_learner_bronze,
            cls.Badge.SUPPORTER_BRONZE: behaviors.check_badge_supporter_bronze,
            cls.Badge.TALKATIVE_BRONZE: behaviors.check_badge_talkative_bronze,
            cls.Badge.TEACHER_BRONZE: behaviors.check_badge_teacher_bronze,
            cls.Badge.VOTER_BRONZE: behaviors.check_badge_voter_bronze,
            cls.Badge.VOTER_GOLD: behaviors.check_badge_voter_gold,
            cls.Badge.VOTER_SILVER: behaviors.check_badge_voter_silver,
            cls.Badge.YEARLING_BRONZE: behaviors.check_badge_yearling_bronze,
        }

    CHOICES_KIND = (
        (Kind.BRONZE.value, _('Bronze')),
        (Kind.GOLD.value, _('Gold')),
        (Kind.SILVER.value, _('Silver')),
    )

    CHOICES_CATEGORY = (
        (Category.ANSWERS.value, _('Answers')),
        (Category.ARTICLES.value, _('Articles')),
        (Category.CHAT.value, _('Chat')),
        (Category.COMMENTS.value, _('Comments')),
        (Category.FORUMS.value, _('Forums')),
        (Category.LIBRARY.value, _('Library')),
        (Category.OPINIONS.value, _('Opinions')),
        (Category.OTHER.value, _('Other')),
        (Category.POLLS.value, _('Polls')),
        (Category.PROFILE.value, _('Profile')),
        (Category.QUESTIONS.value, _('Questions')),
        (Category.SNIPPETS.value, _('Snippets')),
        (Category.SOLUTIONS.value, _('Solutions')),
    )

    CHOICES_NAME = (
        (Badge.AUTOBIOGRAPHER_BRONZE.value, _('Autobiographer')),
        (Badge.BIBLIOPHILE_GOLD.value, _('Bibliophile')),
        (Badge.BOOKLOVER_SILVER.value, _('Booklover')),
        (Badge.CODER_BRONZE.value, _('Coder')),
        (Badge.CODER_GOLD.value, _('Coder')),
        (Badge.CODER_SILVER.value, _('Coder')),
        (Badge.COMMENTATOR_BRONZE.value, _('Commentator')),
        (Badge.COMMENTATOR_GOLD.value, _('Commentator')),
        (Badge.COMMENTATOR_SILVER.value, _('Commentator')),
        (Badge.CRITIC_BRONZE.value, _('Critic')),
        (Badge.ENLIGHTENED_SILVER.value, _('Enlightened')),
        (Badge.ENTHUSIAST_BRONZE.value, _('Enthusiast')),
        (Badge.EPIC_SILVER.value, _('Epic')),
        (Badge.FANATIC_SILVER.value, _('Fanatic')),
        (Badge.FORUMER_SILVER.value, _('Forumer')),
        (Badge.FREQUENT_RECORDER_BRONZE.value, _('Frequent recorder')),
        (Badge.GURU_GOLD.value, _('Guru')),
        (Badge.INITIALIZER_CONVERSATION_BRONZE.value, _('Initializer conversation')),
        (Badge.INTERLOCUTOR_BRONZE.value, _('Interlocutor')),
        (Badge.INVENTOR_BRONZE.value, _('Inventor')),
        (Badge.INVENTOR_GOLD.value, _('Inventor')),
        (Badge.INVENTOR_SILVER.value, _('Inventor')),
        (Badge.LEGENDARY_GOLD.value, _('Legendary')),
        (Badge.OUTSPOKEN_BRONZE.value, _('Outspoken')),
        (Badge.PUBLICIST_BRONZE.value, _('Publicist')),
        (Badge.PUBLICIST_GOLD.value, _('Publicist')),
        (Badge.PUBLICIST_SILVER.value, _('Publicist')),
        (Badge.QUESTIONER_BRONZE.value, _('Questioner')),
        (Badge.QUESTIONER_GOLD.value, _('Questioner')),
        (Badge.QUESTIONER_SILVER.value, _('Questioner')),
        (Badge.READER_BRONZE.value, _('Reader')),
        (Badge.SCHOOLAR_BRONZE.value, _('Schoolar')),
        (Badge.SELF_LEARNER_BRONZE.value, _('Self learner')),
        (Badge.SUPPORTER_BRONZE.value, _('Supporter')),
        (Badge.TALKATIVE_BRONZE.value, _('Talkative')),
        (Badge.TEACHER_BRONZE.value, _('Teacher')),
        (Badge.VOTER_BRONZE.value, _('Voter')),
        (Badge.VOTER_GOLD.value, _('Voter')),
        (Badge.VOTER_SILVER.value, _('Voter')),
        (Badge.YEARLING_BRONZE.value, _('Yearling')),
    )

    CHOICES_DESCRIPTION = (
        (Badge.AUTOBIOGRAPHER_BRONZE.value, _('Filled own profile on more or equal 90%')),
        (Badge.BIBLIOPHILE_GOLD.value, _('Has replies about at least 10 books')),
        (Badge.BOOKLOVER_SILVER.value, _('Has replies about at least 5 books')),
        (Badge.CODER_BRONZE.value, _('Has a snippet with rating more 0 and more at least 100 views')),
        (Badge.CODER_GOLD.value, _('Has a snippet with rating more 50 and more at least 1000 views')),
        (Badge.CODER_SILVER.value, _('Has a snippet with rating more 10 and more at least 500 views')),
        (Badge.COMMENTATOR_BRONZE.value, _('Has at least 10 comments')),
        (Badge.COMMENTATOR_GOLD.value, _('Has at least 100 comments')),
        (Badge.COMMENTATOR_SILVER.value, _('Has at least 50 comments')),
        (Badge.CRITIC_BRONZE.value, _('First down vote')),
        (Badge.ENLIGHTENED_SILVER.value, _('Has a answer with rating at least 10')),
        (Badge.ENTHUSIAST_BRONZE.value, _('Visit the site each day for 30 consecutive days.')),
        (Badge.EPIC_SILVER.value, _('Reputation is more than 1000')),
        (Badge.FANATIC_SILVER.value, _('Visit the site each day for 100 consecutive days.')),
        (Badge.FORUMER_SILVER.value, _('Has at least 10 topics on forum and at least 50 posts')),
        (Badge.FREQUENT_RECORDER_BRONZE.value, _('Has at least 250000 characters in a diary')),
        (Badge.GURU_GOLD.value, _('Has a answer with rating at least 50')),
        (Badge.INITIALIZER_CONVERSATION_BRONZE.value, _('Has a topic on forum')),
        (Badge.INTERLOCUTOR_BRONZE.value, _('Has a post on forum')),
        (Badge.INVENTOR_BRONZE.value, _('Has a solution with rating more 0 and more at least 100 views')),
        (Badge.INVENTOR_GOLD.value, _('Has a solution with rating more 50 and more at least 1000 views')),
        (Badge.INVENTOR_SILVER.value, _('Has a solution with rating more 10 and more at least 500 views')),
        (Badge.LEGENDARY_GOLD.value, _('Reputation is more than 10000')),
        (Badge.OUTSPOKEN_BRONZE.value, _('Has 500 messages in a chat for a day')),
        (Badge.PUBLICIST_BRONZE.value, _('Has article with rating more 0 and views at least 100 views')),
        (Badge.PUBLICIST_GOLD.value, _('Has article with rating more 50 and views at least 1000 views')),
        (Badge.PUBLICIST_SILVER.value, _('Has article with rating more 10 and and views at least 500 views')),
        (Badge.QUESTIONER_BRONZE.value, _('Has a question with rating more 0 and more at least 100 views')),
        (Badge.QUESTIONER_GOLD.value, _('Has a question with rating more 50 and more at least 1000 views')),
        (Badge.QUESTIONER_SILVER.value, _('Has a question with rating more 10 and more at least 500 views')),
        (Badge.READER_BRONZE.value, _('Has reply about a book')),
        (Badge.SCHOOLAR_BRONZE.value, _('Ask a question and accept an answer')),
        (Badge.SELF_LEARNER_BRONZE.value, _('Gave an answer on your own question with rating of 3 or more')),
        (Badge.SUPPORTER_BRONZE.value, _('First up vote')),
        (Badge.TALKATIVE_BRONZE.value, _('Has 100 messages in a chat for a day')),
        (Badge.TEACHER_BRONZE.value, _('Has a answer with rating more 0')),
        (Badge.VOTER_BRONZE.value, _('Has a vote in a poll')),
        (Badge.VOTER_GOLD.value, _('Has a vote in all polls')),
        (Badge.VOTER_SILVER.value, _('Has a vote in more than half count of all polls')),
        (Badge.YEARLING_BRONZE.value, _('More 1 year as registered')),
    )

    _DEFAULT_BADGES = (

        # Comments

        {
            'name': Badge.COMMENTATOR_BRONZE.value,
            'description': Badge.COMMENTATOR_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.COMMENTS.value,
        },
        {
            'name': Badge.COMMENTATOR_SILVER.value,
            'description': Badge.COMMENTATOR_SILVER.value,
            'kind': Kind.SILVER.value,
            'category': Category.COMMENTS.value,
        },
        {
            'name': Badge.COMMENTATOR_GOLD.value,
            'description': Badge.COMMENTATOR_GOLD.value,
            'kind': Kind.GOLD.value,
            'category': Category.COMMENTS.value,
        },

        # Polls
        {
            'name': Badge.VOTER_BRONZE.value,
            'description': Badge.VOTER_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.POLLS.value,
        },
        {
            'name': Badge.VOTER_SILVER.value,
            'description': Badge.VOTER_SILVER.value,
            'kind': Kind.SILVER.value,
            'category': Category.POLLS.value,
        },
        {
            'name': Badge.VOTER_GOLD.value,
            'description': Badge.VOTER_GOLD.value,
            'kind': Kind.GOLD.value,
            'category': Category.POLLS.value,
        },

        # Articles
        {
            'name': Badge.PUBLICIST_BRONZE.value,
            'description': Badge.PUBLICIST_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.ARTICLES.value,
        },
        {
            'name': Badge.PUBLICIST_SILVER.value,
            'description': Badge.PUBLICIST_SILVER.value,
            'kind': Kind.SILVER.value,
            'category': Category.ARTICLES.value,
        },
        {
            'name': Badge.PUBLICIST_GOLD.value,
            'description': Badge.PUBLICIST_GOLD.value,
            'kind': Kind.GOLD.value,
            'category': Category.ARTICLES.value,
        },

        # Snippets
        {
            'name': Badge.CODER_BRONZE.value,
            'description': Badge.CODER_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.SNIPPETS.value,
        },
        {
            'name': Badge.CODER_SILVER.value,
            'description': Badge.CODER_SILVER.value,
            'kind': Kind.SILVER.value,
            'category': Category.SNIPPETS.value,
        },
        {
            'name': Badge.CODER_GOLD.value,
            'description': Badge.CODER_GOLD.value,
            'kind': Kind.GOLD.value,
            'category': Category.SNIPPETS.value,
        },

        # Solutions
        {
            'name': Badge.INVENTOR_BRONZE.value,
            'description': Badge.INVENTOR_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.SOLUTIONS.value,
        },
        {
            'name': Badge.INVENTOR_SILVER.value,
            'description': Badge.INVENTOR_SILVER.value,
            'kind': Kind.SILVER.value,
            'category': Category.SOLUTIONS.value,
        },
        {
            'name': Badge.INVENTOR_GOLD.value,
            'description': Badge.INVENTOR_GOLD.value,
            'kind': Kind.GOLD.value,
            'category': Category.SOLUTIONS.value,
        },

        # Questions
        {
            'name': Badge.QUESTIONER_BRONZE.value,
            'description': Badge.QUESTIONER_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.QUESTIONS.value,
        },
        {
            'name': Badge.QUESTIONER_SILVER.value,
            'description': Badge.QUESTIONER_SILVER.value,
            'kind': Kind.SILVER.value,
            'category': Category.QUESTIONS.value,
        },
        {
            'name': Badge.QUESTIONER_GOLD.value,
            'description': Badge.QUESTIONER_GOLD.value,
            'kind': Kind.GOLD.value,
            'category': Category.QUESTIONS.value,
        },


        {
            'name': Badge.TEACHER_BRONZE.value,
            'description': Badge.TEACHER_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.ANSWERS.value,
        },
        {
            'name': Badge.ENLIGHTENED_SILVER.value,
            'description': Badge.ENLIGHTENED_SILVER.value,
            'kind': Kind.SILVER.value,
            'category': Category.ANSWERS.value,
        },
        {
            'name': Badge.GURU_GOLD.value,
            'description': Badge.GURU_GOLD.value,
            'kind': Kind.GOLD.value,
            'category': Category.ANSWERS.value,
        },
        {
            'name': Badge.SELF_LEARNER_BRONZE.value,
            'description': Badge.SELF_LEARNER_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.ANSWERS.value,
        },
        {
            'name': Badge.SCHOOLAR_BRONZE.value,
            'description': Badge.SCHOOLAR_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.ANSWERS.value,
        },

        # Forums
        {
            'name': Badge.INTERLOCUTOR_BRONZE.value,
            'description': Badge.INTERLOCUTOR_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.FORUMS.value,
        },
        {
            'name': Badge.INITIALIZER_CONVERSATION_BRONZE.value,
            'description': Badge.INITIALIZER_CONVERSATION_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.FORUMS.value,
        },
        {
            'name': Badge.FORUMER_SILVER.value,
            'description': Badge.FORUMER_SILVER.value,
            'kind': Kind.SILVER.value,
            'category': Category.FORUMS.value,
        },

        # Other
        {
            'name': Badge.ENTHUSIAST_BRONZE.value,
            'description': Badge.ENTHUSIAST_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.OTHER.value,
        },
        {
            'name': Badge.FREQUENT_RECORDER_BRONZE.value,
            'description': Badge.FREQUENT_RECORDER_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.OTHER.value,
        },
        {
            'name': Badge.FANATIC_SILVER.value,
            'description': Badge.FANATIC_SILVER.value,
            'kind': Kind.SILVER.value,
            'category': Category.OTHER.value,
        },
        {
            'name': Badge.EPIC_SILVER.value,
            'description': Badge.EPIC_SILVER.value,
            'kind': Kind.SILVER.value,
            'category': Category.OTHER.value,
        },
        {
            'name': Badge.LEGENDARY_GOLD.value,
            'description': Badge.LEGENDARY_GOLD.value,
            'kind': Kind.GOLD.value,
            'category': Category.OTHER.value,
        },
        {
            'name': Badge.YEARLING_BRONZE.value,
            'description': Badge.YEARLING_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.OTHER.value,
        },

        # Profile
        {
            'name': Badge.AUTOBIOGRAPHER_BRONZE.value,
            'description': Badge.AUTOBIOGRAPHER_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.PROFILE.value,
        },

        # Opinions
        {
            'name': Badge.CRITIC_BRONZE.value,
            'description': Badge.CRITIC_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.OPINIONS.value,
        },
        {
            'name': Badge.SUPPORTER_BRONZE.value,
            'description': Badge.SUPPORTER_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.OPINIONS.value,
        },

        # Chat
        {
            'name': Badge.TALKATIVE_BRONZE.value,
            'description': Badge.TALKATIVE_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.CHAT.value,
        },

        {
            'name': Badge.OUTSPOKEN_BRONZE.value,
            'description': Badge.OUTSPOKEN_BRONZE.value,
            'kind': Kind.SILVER.value,
            'category': Category.CHAT.value,
        },

        # Library
        {
            'name': Badge.READER_BRONZE.value,
            'description': Badge.READER_BRONZE.value,
            'kind': Kind.BRONZE.value,
            'category': Category.LIBRARY.value,
        },
        {
            'name': Badge.BOOKLOVER_SILVER.value,
            'description': Badge.BOOKLOVER_SILVER.value,
            'kind': Kind.SILVER.value,
            'category': Category.LIBRARY.value,
        },
        {
            'name': Badge.BIBLIOPHILE_GOLD.value,
            'description': Badge.BIBLIOPHILE_GOLD.value,
            'kind': Kind.GOLD.value,
            'category': Category.LIBRARY.value,
        },

    )
