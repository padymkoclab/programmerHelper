
import enum

from django.utils.translation import ugettext as _


@enum.unique
class Actions(enum.Enum):
    """

    """

    # users
    REGISTRED_USER = 'registred_user'
    UPDATED_USER = 'updated_user'
    DELETED_USER = 'deleted_user'
    UPDATED_PROFILE = 'updated_profile'
    USER_LOGGED_IN = 'user_logged_in'
    USER_LOGGED_OUT = 'user_logged_out'
    USER_LOGIN_FAILED = 'user_loggin_failed'
    USER_ADDED_TO_GROUP = 'user_added_to_group'
    USER_REMOVED_FROM_GROUP = 'user_removed_from_group'

    # snippets
    ADDED_SNIPPET = 'added_snippet'
    UPDATED_SNIPPET = 'updated_snippet'
    DELETED_SNIPPET = 'deleted snippet'

    # articles
    ADDED_ARTICLE = 'added_article'
    UPDATED_ARTICLE = 'updated_article'
    DELETED_ARTICLE = 'deleted article'
    ADDED_MARK = 'added_mark'
    UPDATED_MARK = 'updated_mark'
    DELETED_MARK = 'deleted_mark'

    # solutions
    ADDED_SOLUTION = 'added_solution'
    UPDATED_SOLUTION = 'updated_solution'
    DELETED_SOLUTION = 'deleted solution'

    # questions
    ADDED_QUESTION = 'added_question'
    UPDATED_QUESTION = 'updated_question'
    DELETED_QUESTION = 'deleted question'
    ADDED_ANSWER = 'added_answer'
    UPDATED_ANSWER = 'updated_answer'
    DELETED_ANSWER = 'deleted_answer'

    # forums
    ADDED_TOPIC = 'added_topic'
    UPDATED_TOPIC = 'updated_topic'
    DELETED_TOPIC = 'deleted topic'
    ADDED_POST = 'added_post'
    UPDATED_POST = 'updated_post'
    DELETED_POST = 'deleted_post'

    # polls
    ADDED_VOTE = 'added_vote'
    UPDATED_VOTE = 'updated_vote'
    DELETED_VOTE = 'deleted_vote'

    # opinions
    ADDED_OPINION = 'added_opinion'
    UPDATED_OPINION = 'updated_opinion'
    DELETED_OPINION = 'deleted_opinion'

    # comments
    ADDED_COMMENT = 'added_comment'
    UPDATED_COMMENT = 'updated_comment'
    DELETED_COMMENT = 'deleted_comment'

    # library
    ADDED_REPLY = 'added_reply'
    UPDATED_REPLY = 'updated_reply'
    DELETED_REPLY = 'deleted_reply'

    # badge
    EARNED_BADGE = 'earned_badge'
    LOST_BADGE = 'lost_badge'

    # plugable apps
    ACTIVATED_DIARY = 'activated_diary'
    UPDATED_DIARY = 'updated_diary'
    DEACTIVATED_DIARY = 'deactivated_diary'
    ACTIVATED_CALENDAR = 'activated_calendar'
    DEACTIVATED_CALENDAR = 'deactivated_calendar'

    # user`s reputation
    REPUTATION_PARTICIPATE_IN_POLL = 'reputation_participate_in_poll'
    REPUTATION_UNDO_PARTICIPATE_IN_POLL = 'reputation_undo_participate_in_poll'
    REPUTATION_UPVOTE_OPINION = 'reputation_upvote'
    REPUTATION_CHANGED_TO_UPVOTE_OPINION = 'reputation_change_to_upvote'
    REPUTATION_DOWNVOTE_OPINION = 'reputation_downvote'
    REPUTATION_CHANGED_TO_DOWNVOTE_OPINION = 'reputation_change_to_downvote'
    REPUTATION_LOSE_UPVOTE_OPINION = 'reputation_lose_upvote'
    REPUTATION_LOSE_DOWNVOTE_OPINION = 'reputation_lose_downvote'
    REPUTATION_PUT_ASSESSMENT = 'reputation_put_assessment'
    REPUTATION_CHANGED_ASSESSMENT_TO_UP = 'reputation_changed_assessment_to_up'
    REPUTATION_CHANGED_ASSESSMENT_TO_DOWN = 'reputation_changed_assessment_to_down'
    REPUTATION_UNDO_ASSESSMENT = 'reputation_undo_assessment'

    _CHOICES = {

        # users
        REGISTRED_USER: _('registred new %(actor_type)s %(actor)s'),
        UPDATED_USER: _('%(actor)s updated own data'),
        UPDATED_PROFILE: _('%(actor)s updated profile'),
        DELETED_USER: _('deleted %(actor_type)s %(actor)s'),
        USER_LOGGED_IN: _('%(actor)s logged in'),
        USER_LOGGED_OUT: _('%(actor)s logged out'),
        USER_LOGIN_FAILED: _('%(actor)s loggin failed'),
        USER_ADDED_TO_GROUP: _('%(actor)s added to %(target_type)s "%(target)s"'),
        USER_REMOVED_FROM_GROUP: _('%(actor)s removed from %(target_type)s "%(target)s"'),

        # snippets
        ADDED_SNIPPET: _('%(actor)s added %(target_type)s "%(target)s"'),
        UPDATED_SNIPPET: _('%(actor)s updated %(target_type)s "%(target)s"'),
        DELETED_SNIPPET: _('%(actor)s deleted %(target_type)s "%(target)s"'),

        # articles
        ADDED_ARTICLE: _('%(actor)s added %(target_type)s "%(target)s"'),
        UPDATED_ARTICLE: _('%(actor)s updated %(target_type)s "%(target)s"'),
        DELETED_ARTICLE: _('%(actor)s deleted %(target_type)s "%(target)s"'),
        ADDED_MARK: _('%(actor)s added %(target_type)s "%(target)s"'),
        UPDATED_MARK: _('%(actor)s updated %(target_type)s "%(target)s"'),
        DELETED_MARK: _('%(actor)s deleted %(target_type)s "%(target)s"'),

        # solutions
        ADDED_SOLUTION: _('%(actor)s  added %(target_type)s "%(target)s"'),
        UPDATED_SOLUTION: _('%(actor)s updated %(target_type)s "%(target)s"'),
        DELETED_SOLUTION: _('%(actor)s deleted %(target_type)s "%(target)s"'),

        # questions
        ADDED_QUESTION: _('%(actor)s  added %(target_type)s "%(target)s"'),
        UPDATED_QUESTION: _('%(actor)s updated %(target_type)s "%(target)s"'),
        DELETED_QUESTION: _('%(actor)s deleted %(target_type)s "%(target)s"'),
        ADDED_ANSWER: _('%(actor)s  added %(target_type)s "%(target)s"'),
        UPDATED_ANSWER: _('%(actor)s updated %(target_type)s "%(target)s"'),
        DELETED_ANSWER: _('%(actor)s deleted %(target_type)s "%(target)s"'),

        # forums
        ADDED_TOPIC: _('%(actor)s  added %(target_type)s "%(target)s"'),
        UPDATED_TOPIC: _('%(actor)s updated %(target_type)s "%(target)s"'),
        DELETED_TOPIC: _('%(actor)s deleted %(target_type)s "%(target)s"'),
        ADDED_POST: _('%(actor)s  added %(target_type)s "%(target)s"'),
        UPDATED_POST: _('%(actor)s updated %(target_type)s "%(target)s"'),
        DELETED_POST: _('%(actor)s deleted %(target_type)s "%(target)s"'),

        # polls
        ADDED_VOTE: _('%(actor)s added %(action_target_type)s on %(target_type)s "%(target)s"'),
        UPDATED_VOTE: _('%(actor)s updated %(action_target_type)s on %(target_type)s "%(target)s"'),
        DELETED_VOTE: _('%(actor)s deleted %(action_target_type)s on %(target_type)s "%(target)s"'),

        # opinions
        ADDED_OPINION: _('%(actor)s added %(action_target_type)s on %(target_type)s "%(target)s'),
        UPDATED_OPINION: _('%(actor)s updated %(action_target_type)s on %(target_type)s "%(target)s'),
        DELETED_OPINION: _('%(actor)s deleted %(action_target_type)s on %(target_type)s "%(target)s'),

        # comments
        ADDED_COMMENT: _('%(actor)s added %(action_target_type)s on %(target_type)s "%(target)s'),
        UPDATED_COMMENT: _('%(actor)s updated %(action_target_type)s on %(target_type)s "%(target)s'),
        DELETED_COMMENT: _('%(actor)s deleted %(action_target_type)s on %(target_type)s "%(target)s'),

        # library
        ADDED_REPLY: _('%(actor)s added %(action_target_type)s on %(target_type)s "%(target)s'),
        UPDATED_REPLY: _('%(actor)s updated %(action_target_type)s on %(target_type)s "%(target)s'),
        DELETED_REPLY: _('%(actor)s deleted %(action_target_type)s on %(target_type)s "%(target)s'),

        # badge
        EARNED_BADGE: _('%(actor)s earned %(target_type)s "%(target)s"'),
        LOST_BADGE: _('%(actor)s lost %(target_type)s "%(target)s"'),

        # plugable apps
        ACTIVATED_DIARY: _('%(actor)s activated %(target_type)s'),
        UPDATED_DIARY: _('%(actor)s updated %(target_type)s'),
        DEACTIVATED_DIARY: _('%(actor)s deactivated %(target_type)s'),
        ACTIVATED_CALENDAR: _('%(actor)s activated %(target_type)s'),
        DEACTIVATED_CALENDAR: _('%(actor)s deactivated %(target_type)s'),

        # user`s reputation
        REPUTATION_PARTICIPATE_IN_POLL: _('reputation of %(recipient)s was changed on %(reputation_deviation)s'),
        REPUTATION_UNDO_PARTICIPATE_IN_POLL: _('reputation of %(recipient)s was changed on %(reputation_deviation)s'),
        REPUTATION_UPVOTE_OPINION: _('reputation of %(recipient)s was changed on %(reputation_deviation)s'),
        REPUTATION_CHANGED_TO_UPVOTE_OPINION: _('reputation of %(recipient)s was changed on %(reputation_deviation)s'),
        REPUTATION_DOWNVOTE_OPINION: _('reputation of %(recipient)s was changed on %(reputation_deviation)s'),
        REPUTATION_CHANGED_TO_DOWNVOTE_OPINION: _('reputation of %(recipient)s was changed on %(reputation_deviation)s'),
        REPUTATION_LOSE_UPVOTE_OPINION: _('reputation of %(recipient)s was changed on %(reputation_deviation)s'),
        REPUTATION_LOSE_DOWNVOTE_OPINION: _('reputation of %(recipient)s was changed on %(reputation_deviation)s'),
        REPUTATION_PUT_ASSESSMENT: _('reputation of %(recipient)s was changed on %(reputation_deviation)s'),
        REPUTATION_CHANGED_ASSESSMENT_TO_UP: _('reputation of %(recipient)s was changed on %(reputation_deviation)s'),
        REPUTATION_CHANGED_ASSESSMENT_TO_DOWN: _('reputation of %(recipient)s was changed on %(reputation_deviation)s'),
        REPUTATION_UNDO_ASSESSMENT: _('reputation of %(recipient)s was changed on %(reputation_deviation)s'),
    }

    @classmethod
    def get_action_display_pattern(cls, action_key):
        """ """

        try:
            return cls._CHOICES.value[action_key]
        except KeyError:
            raise ValueError('Action with key "{}" does not exists'.format(action_key))

    @classmethod
    def get_reputation_deviation(cls, action_key):

        from apps.polls.models import Poll
        from apps.questions.models import Question, Answer
        from apps.articles.models import Article
        from apps.solutions.models import Solution
        from apps.snippets.models import Snippet

        reputation_charge = {
            Poll: 1,
            Solution: 3,
            Question: 2,
            Answer: 3,
            Snippet: 2,
            Article: 'mark',
        }
        raise NotImplementedError('Need bind for type object and type action')
        {
            cls.REPUTATION_PARTICIPATE_IN_POLL: '+',
            cls.REPUTATION_UNDO_PARTICIPATE_IN_POLL: '-',
            cls.REPUTATION_UPVOTE_OPINION: '+',
            cls.REPUTATION_CHANGED_TO_UPVOTE_OPINION: '+',
            cls.REPUTATION_DOWNVOTE_OPINION: '-',
            cls.REPUTATION_CHANGED_TO_DOWNVOTE_OPINION: '-',
            cls.REPUTATION_LOSE_UPVOTE_OPINION: '-',
            cls.REPUTATION_LOSE_DOWNVOTE_OPINION: '+',
            cls.REPUTATION_PUT_ASSESSMENT: '+',
            cls.REPUTATION_CHANGED_ASSESSMENT_TO_UP: '+',
            cls.REPUTATION_CHANGED_ASSESSMENT_TO_DOWN: '-',
            cls.REPUTATION_UNDO_ASSESSMENT: '-',
        }
        try:
            const = cls(action_key)
        except ValueError:
            return
        return reputation_charge.get(const)
