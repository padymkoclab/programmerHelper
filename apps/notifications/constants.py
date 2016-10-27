
import logging

from django.utils.translation import ugettext_lazy as _

from utils.python.utils import classproperty


logger = logging.getLogger('django.development')


class Action(object):
    """

    """

    ADDED_OBJECT = 'added'
    ADDED_USER = 'added_user'
    ADDED_BADGE = 'earned_badge'
    ADDED_VOTE = 'added_vote'
    ADDED_OPINION = 'added_opinion'
    ADDED_COMMENT = 'added_comment'
    ADDED_MARK = 'added_mark'
    ADDED_ANSWER = 'added_answer'
    ADDED_REPLY = 'added_reply'
    ADDED_POST = 'added_post'

    UPDATED_OBJECT = 'updated'
    UPDATED_USER = 'updated_user'
    UPDATED_VOTE = 'updated_vote'
    UPDATED_OPINION = 'updated_opinion'
    UPDATED_COMMENT = 'updated_comment'
    UPDATED_MARK = 'updated_mark'
    UPDATED_ANSWER = 'updated_answer'
    UPDATED_REPLY = 'updated_reply'
    UPDATED_POST = 'updated_post'
    UPDATED_PROFILE = 'updated_profile'
    UPDATED_DIARY = 'updated_diary'
    UPDATED_REPUTATION = 'updated_reputation'

    DELETED_OBJECT = 'deleted'
    DELETED_USER = 'deleted_user'
    DELETED_BADGE = 'lost_badge'
    DELETED_VOTE = 'deleted_vote'
    DELETED_OPINION = 'deleted_opinion'
    DELETED_COMMENT = 'deleted_comment'
    DELETED_MARK = 'deleted_mark'
    DELETED_ANSWER = 'deleted_answer'
    DELETED_REPLY = 'deleted_reply'
    DELETED_POST = 'deleted_post'
    DELETED_ANSWER = 'deleted_answer'
    DELETED_VOTE = 'deleted_vote'

    USER_LOGGED_IN = 'user_logged_in'
    USER_LOGGED_OUT = 'user_logged_out'

    ADDED_ACTION_TITLE = 'added_action_title'
    UPDATED_ACTION_TITLE = 'updated_action_title'
    DELETED_ACTION_TITLE = 'deleted_action_title'

    _ACTION_TITLES = {
        ADDED_ACTION_TITLE: _('New'),
        UPDATED_ACTION_TITLE: _('Updated'),
        DELETED_ACTION_TITLE: _('Deleted'),
        USER_LOGGED_IN: _('Successful loggin'),
        USER_LOGGED_OUT: _('Successful logout'),
    }

    logger.info('Will write checkup_undublicate_keys()')

    @classproperty
    def choices(cls):

        return {

            cls.ADDED_OBJECT: _('added'),
            cls.ADDED_USER: _('registered'),
            cls.ADDED_BADGE: _('earned badge'),
            cls.ADDED_VOTE: _('added vote to'),
            cls.ADDED_OPINION: _('added opinion to'),
            cls.ADDED_COMMENT: _('added comment to'),
            cls.ADDED_MARK: _('added mark to'),
            cls.ADDED_ANSWER: _('added answer to'),
            cls.ADDED_REPLY: _('added reply to'),
            cls.ADDED_POST: _('added post to'),

            cls.UPDATED_OBJECT: _('updated'),
            cls.UPDATED_USER: _('updated'),
            cls.UPDATED_VOTE: _('updated vote to'),
            cls.UPDATED_OPINION: _('updated opinion to'),
            cls.UPDATED_COMMENT: _('updated comment to'),
            cls.UPDATED_MARK: _('updated mark to'),
            cls.UPDATED_ANSWER: _('updated answer to'),
            cls.UPDATED_REPLY: _('updated reply to'),
            cls.UPDATED_POST: _('updated post to'),
            cls.UPDATED_REPUTATION: _('updated reputation'),
            cls.UPDATED_PROFILE: _('updated profile'),
            cls.UPDATED_DIARY: _('updated diary'),

            cls.DELETED_OBJECT: _('deleted'),
            cls.DELETED_USER: _('deleted'),
            cls.DELETED_BADGE: _('deleted'),
            cls.DELETED_VOTE: _('deleted vote to'),
            cls.DELETED_OPINION: _('deleted opinion to'),
            cls.DELETED_COMMENT: _('deleted comment to'),
            cls.DELETED_MARK: _('deleted mark to'),
            cls.DELETED_ANSWER: _('deleted answer to'),
            cls.DELETED_REPLY: _('deleted reply to'),
            cls.DELETED_POST: _('deleted post to'),

            cls.USER_LOGGED_IN: _('logged in'),
            cls.USER_LOGGED_OUT: _('logged out'),
        }

    @classmethod
    def get_action_display(cls, action_key):
        """ """

        try:
            return cls.choices[action_key]
        except KeyError:
            raise ValueError('Action with key {} does not exists'.format(action_key))

    @classmethod
    def get_type_action_title(cls, action_key):

        if action_key.startswith('added'):
            return cls.ADDED_ACTION_TITLE
        elif action_key.startswith('updated'):
            return cls.UPDATED_ACTION_TITLE
        elif action_key.startswith('deleted'):
            return cls.DELETED_ACTION_TITLE
        else:

            try:
                return cls._ACTION_TITLES[action_key]
            except KeyError:
                raise ValueError('Unregisted action key {}.'.format(action_key))
