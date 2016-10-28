
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
        QUESTIONS = 'questions'
        ARTICLES = 'articles'
        SOLUTIONS = 'solutions'
        SNIPPETS = 'snippets'
        POLLS = 'polls'
        FORUMS = 'forums'
        OPINIONS = 'opinions'
        COMMENTS = 'comments'
        PROFILE = 'profile'
        OTHER = 'other'
        CHAT = 'chat'

    @enum.unique
    class Badge(enum.Enum):

        AUTOBIOGRAPHER_BRONZE = 'autobiographer_bronze'
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
        SILVER = 'silver'
        GOLD = 'gold'

    @classproperty
    def checkers(cls):

        return {
            cls.Badge.COMMENTATOR_BRONZE: behaviors.check_badge_commentator_bronze,
            cls.Badge.COMMENTATOR_SILVER: behaviors.check_badge_commentator_silver,
            cls.Badge.COMMENTATOR_GOLD: behaviors.check_badge_commentator_gold,
            cls.Badge.VOTER_BRONZE: behaviors.check_badge_voter_bronze,
            cls.Badge.VOTER_SILVER: behaviors.check_badge_voter_silver,
            cls.Badge.VOTER_GOLD: behaviors.check_badge_voter_gold,
            cls.Badge.PUBLICIST_BRONZE: behaviors.check_badge_publicist_bronze,
            cls.Badge.PUBLICIST_SILVER: behaviors.check_badge_publicist_silver,
            cls.Badge.PUBLICIST_GOLD: behaviors.check_badge_publicist_gold,
            cls.Badge.CODER_BRONZE: behaviors.check_badge_coder_bronze,
            cls.Badge.CODER_SILVER: behaviors.check_badge_coder_silver,
            cls.Badge.CODER_GOLD: behaviors.check_badge_coder_gold,
            cls.Badge.INVENTOR_BRONZE: behaviors.check_badge_inventor_bronze,
            cls.Badge.INVENTOR_SILVER: behaviors.check_badge_inventor_silver,
            cls.Badge.INVENTOR_GOLD: behaviors.check_badge_inventor_gold,
            cls.Badge.QUESTIONER_BRONZE: behaviors.check_badge_questioner_bronze,
            cls.Badge.QUESTIONER_SILVER: behaviors.check_badge_questioner_silver,
            cls.Badge.QUESTIONER_GOLD: behaviors.check_badge_questioner_gold,
            cls.Badge.TEACHER_BRONZE: behaviors.check_badge_teacher_bronze,
            cls.Badge.ENLIGHTENED_SILVER: behaviors.check_badge_enlightened_silver,
            cls.Badge.GURU_GOLD: behaviors.check_badge_guru_gold,
            cls.Badge.SELF_LEARNER_BRONZE: behaviors.check_badge_self_learner_bronze,
            cls.Badge.SCHOOLAR_BRONZE: behaviors.check_badge_schoolar_bronze,
            cls.Badge.INTERLOCUTOR_BRONZE: behaviors.check_badge_interlocutor_bronze,
            cls.Badge.INITIALIZER_CONVERSATION_BRONZE: behaviors.check_badge_initializer_conversation_bronze,
            cls.Badge.FORUMER_SILVER: behaviors.check_badge_forumer_silver,
            cls.Badge.ENTHUSIAST_BRONZE: behaviors.check_badge_enthusiast_bronze,
            cls.Badge.FREQUENT_RECORDER_BRONZE: behaviors.check_badge_frequent_recorder_bronze,
            cls.Badge.FANATIC_SILVER: behaviors.check_badge_fanatic_silver,
            cls.Badge.EPIC_SILVER: behaviors.check_badge_epic_silver,
            cls.Badge.LEGENDARY_GOLD: behaviors.check_badge_legendary_gold,
            cls.Badge.YEARLING_BRONZE: behaviors.check_badge_yearling_bronze,
            cls.Badge.AUTOBIOGRAPHER_BRONZE: behaviors.check_badge_autobiographer_bronze,
            cls.Badge.CRITIC_BRONZE: behaviors.check_badge_critic_bronze,
            cls.Badge.SUPPORTER_BRONZE: behaviors.check_badge_supporter_bronze,
            cls.Badge.OUTSPOKEN_BRONZE: behaviors.check_badge_outspoken_bronze,
            cls.Badge.TALKATIVE_BRONZE: behaviors.check_badge_talkative_bronze,
        }

    CHOICES_KIND = (
        (Kind.BRONZE.value, _('Bronze')),
        (Kind.SILVER.value, _('Silver')),
        (Kind.GOLD.value, _('Gold')),
    )

    CHOICES_CATEGORY = (
        (Category.ANSWERS.value, _('Answers')),
        (Category.QUESTIONS.value, _('Questions')),
        (Category.ARTICLES.value, _('Articles')),
        (Category.SOLUTIONS.value, _('Solutions')),
        (Category.SNIPPETS.value, _('Snippets')),
        (Category.POLLS.value, _('Polls')),
        (Category.FORUMS.value, _('Forums')),
        (Category.OPINIONS.value, _('Opinions')),
        (Category.COMMENTS.value, _('Comments')),
        (Category.PROFILE.value, _('Profile')),
        (Category.CHAT.value, _('Chat')),
        (Category.OTHER.value, _('Other')),
    )

    CHOICES_NAME = (
        (Badge.COMMENTATOR_BRONZE.value, _('Commentator')),
        (Badge.COMMENTATOR_SILVER.value, _('Commentator')),
        (Badge.COMMENTATOR_GOLD.value, _('Commentator')),
        (Badge.VOTER_BRONZE.value, _('Voter')),
        (Badge.VOTER_SILVER.value, _('Voter')),
        (Badge.VOTER_GOLD.value, _('Voter')),
        (Badge.PUBLICIST_BRONZE.value, _('Publicist')),
        (Badge.PUBLICIST_SILVER.value, _('Publicist')),
        (Badge.PUBLICIST_GOLD.value, _('Publicist')),
        (Badge.CODER_BRONZE.value, _('Coder')),
        (Badge.CODER_SILVER.value, _('Coder')),
        (Badge.CODER_GOLD.value, _('Coder')),
        (Badge.INVENTOR_BRONZE.value, _('Inventor')),
        (Badge.INVENTOR_SILVER.value, _('Inventor')),
        (Badge.INVENTOR_GOLD.value, _('Inventor')),
        (Badge.QUESTIONER_BRONZE.value, _('Questioner')),
        (Badge.QUESTIONER_SILVER.value, _('Questioner')),
        (Badge.QUESTIONER_GOLD.value, _('Questioner')),
        (Badge.TEACHER_BRONZE.value, _('Teacher')),
        (Badge.ENLIGHTENED_SILVER.value, _('Enlightened')),
        (Badge.GURU_GOLD.value, _('Guru')),
        (Badge.SELF_LEARNER_BRONZE.value, _('Self learner')),
        (Badge.SCHOOLAR_BRONZE.value, _('Schoolar')),
        (Badge.INTERLOCUTOR_BRONZE.value, _('Interlocutor')),
        (Badge.INITIALIZER_CONVERSATION_BRONZE.value, _('Initializer conversation')),
        (Badge.FORUMER_SILVER.value, _('Forumer')),
        (Badge.ENTHUSIAST_BRONZE.value, _('Enthusiast')),
        (Badge.FREQUENT_RECORDER_BRONZE.value, _('Frequent recorder')),
        (Badge.FANATIC_SILVER.value, _('Fanatic')),
        (Badge.EPIC_SILVER.value, _('Epic')),
        (Badge.LEGENDARY_GOLD.value, _('Legendary')),
        (Badge.YEARLING_BRONZE.value, _('Yearling')),
        (Badge.AUTOBIOGRAPHER_BRONZE.value, _('Autobiographer')),
        (Badge.CRITIC_BRONZE.value, _('Critic')),
        (Badge.SUPPORTER_BRONZE.value, _('Supporter')),
        (Badge.OUTSPOKEN_BRONZE.value, _('Outspoken')),
        (Badge.TALKATIVE_BRONZE.value, _('Talkative')),
    )

    CHOICES_DESCRIPTION = (
        (Badge.COMMENTATOR_BRONZE.value, _('Has 10 comments')),
        (Badge.COMMENTATOR_SILVER.value, _('Has 50 comments')),
        (Badge.COMMENTATOR_GOLD.value, _('Has 100 comments')),
        (Badge.VOTER_BRONZE.value, _('Has a vote in a poll')),
        (Badge.VOTER_SILVER.value, _('Has a vote in more than half count of all polls')),
        (Badge.VOTER_GOLD.value, _('Has a vote in all polls')),
        (Badge.PUBLICIST_BRONZE.value, _('Has article with rating more 0 and views more 100')),
        (Badge.PUBLICIST_SILVER.value, _('Has article with rating more 10 and and views more 500')),
        (Badge.PUBLICIST_GOLD.value, _('Has article with rating more 50 and views more 1000')),
        (Badge.CODER_BRONZE.value, _('Has a snippet with rating more 0 and more 100 views')),
        (Badge.CODER_SILVER.value, _('Has a snippet with rating more 10 and more 500 views')),
        (Badge.CODER_GOLD.value, _('Has a snippet with rating more 50 and more 1000 views')),
        (Badge.INVENTOR_BRONZE.value, _('Has a solution with rating more 0 and more 100 views')),
        (Badge.INVENTOR_SILVER.value, _('Has a solution with rating more 10 and more 500 views')),
        (Badge.INVENTOR_GOLD.value, _('Has a solution with rating more 50 and more 1000 views')),
        (Badge.QUESTIONER_BRONZE.value, _('Has a question with rating more 0 and more 100 views')),
        (Badge.QUESTIONER_SILVER.value, _('Has a question with rating more 10 and more 500 views')),
        (Badge.QUESTIONER_GOLD.value, _('Has a question with rating more 50 and more 1000 views')),
        (Badge.TEACHER_BRONZE.value, _('Has a answer with ration more 0')),
        (Badge.ENLIGHTENED_SILVER.value, _('Has a answer with rating more 10')),
        (Badge.GURU_GOLD.value, _('Has a answer with rating more 50')),
        (Badge.SELF_LEARNER_BRONZE.value, _('Gave an answer on your own question with rating of 3 or more')),
        (Badge.SCHOOLAR_BRONZE.value, _('Ask a question and accept an answer')),
        (Badge.INTERLOCUTOR_BRONZE.value, _('Has a post on forum')),
        (Badge.INITIALIZER_CONVERSATION_BRONZE.value, _('Has a topic on forum')),
        (Badge.FORUMER_SILVER.value, _('Has at least 10 topics on forum and at least 50 posts')),
        (Badge.ENTHUSIAST_BRONZE.value, _('Visit the site each day for 30 consecutive days.')),
        (Badge.FREQUENT_RECORDER_BRONZE.value, _('Has at least 250000 characters in a diary')),
        (Badge.FANATIC_SILVER.value, _('Visit the site each day for 100 consecutive days.')),
        (Badge.EPIC_SILVER.value, _('Reputation is more than 1000')),
        (Badge.LEGENDARY_GOLD.value, _('Reputation is more than 10000')),
        (Badge.YEARLING_BRONZE.value, _('More 1 year as registered')),
        (Badge.AUTOBIOGRAPHER_BRONZE.value, _('Filled own profile on more or equal 90%')),
        (Badge.CRITIC_BRONZE.value, _('First down vote')),
        (Badge.SUPPORTER_BRONZE.value, _('First up vote')),
        (Badge.TALKATIVE_BRONZE.value, _('Has 100 messages in a chat for a day')),
        (Badge.OUTSPOKEN_BRONZE.value, _('Has 500 messages in a chat for a day')),
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
            'category': Category.PROFILE.value,
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

    )
