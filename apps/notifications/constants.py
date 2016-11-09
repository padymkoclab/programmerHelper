
import enum

from django.utils.translation import ugettext_lazy as _


@enum.unique
class Actions(enum.Enum):
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
    DELETED_OPINION = 'deleted_opinion'
    DELETED_COMMENT = 'deleted_comment'
    DELETED_MARK = 'deleted_mark'
    DELETED_REPLY = 'deleted_reply'
    DELETED_POST = 'deleted_post'
    DELETED_ANSWER = 'deleted_answer'
    DELETED_VOTE = 'deleted_vote'

    USER_LOGGED_IN = 'user_logged_in'
    USER_LOGGED_OUT = 'user_logged_out'
    USER_LOGIN_FAILED = 'user_loggin_failed'

    USER_ADDED_TO_GROUP = 'user_added_to_group'
    USER_REMOVED_FROM_GROUP = 'user_removed_from_group'

    ADDED_ACTION_TITLE = 'added_action_title'
    UPDATED_ACTION_TITLE = 'updated_action_title'
    DELETED_ACTION_TITLE = 'deleted_action_title'

    _TITLES = {
        ADDED_ACTION_TITLE: (_('New'), True),
        UPDATED_ACTION_TITLE: (_('Updated'), True),
        DELETED_ACTION_TITLE: (_('Deleted'), True),
        USER_LOGGED_IN: (_('Successful loggin'), False),
        USER_LOGGED_OUT: (_('Successful logout'), False),
        USER_LOGIN_FAILED: (_('Failed loggin'), False),
        ADDED_BADGE: (_('Earned a badge'), False),
        DELETED_BADGE: (_('Lost the badge'), False),
        USER_ADDED_TO_GROUP: (_('added to'), True),
        USER_REMOVED_FROM_GROUP: (_('removed from'), True),
    }

    _CHOICES = {
        ADDED_OBJECT: _('added'),
        ADDED_USER: _('registered'),
        ADDED_BADGE: _('earned'),
        ADDED_VOTE: _('added vote to'),
        ADDED_OPINION: _('added opinion to'),
        ADDED_COMMENT: _('added comment to'),
        ADDED_MARK: _('added mark to'),
        ADDED_ANSWER: _('added answer to'),
        ADDED_REPLY: _('added reply to'),
        ADDED_POST: _('added post to'),

        UPDATED_OBJECT: _('updated'),
        UPDATED_USER: _('updated'),
        UPDATED_VOTE: _('updated vote to'),
        UPDATED_OPINION: _('updated opinion to'),
        UPDATED_COMMENT: _('updated comment to'),
        UPDATED_MARK: _('updated mark to'),
        UPDATED_ANSWER: _('updated answer to'),
        UPDATED_REPLY: _('updated reply to'),
        UPDATED_POST: _('updated post to'),
        UPDATED_REPUTATION: _('updated reputation'),
        UPDATED_PROFILE: _('updated profile'),
        UPDATED_DIARY: _('updated diary'),

        DELETED_OBJECT: _('deleted'),
        DELETED_USER: _('deleted'),
        DELETED_BADGE: _('lost'),
        DELETED_VOTE: _('deleted vote to'),
        DELETED_OPINION: _('deleted opinion to'),
        DELETED_COMMENT: _('deleted comment to'),
        DELETED_MARK: _('deleted mark to'),
        DELETED_ANSWER: _('deleted answer to'),
        DELETED_REPLY: _('deleted reply to'),
        DELETED_POST: _('deleted post to'),

        USER_LOGGED_IN: _('logged in'),
        USER_LOGGED_OUT: _('logged out'),
        USER_LOGIN_FAILED: _('failed loggin'),

        USER_ADDED_TO_GROUP: _('added to'),
        USER_REMOVED_FROM_GROUP: _('removed from'),
    }

    @classmethod
    def get_action_display(cls, action_key):
        """ """

        try:
            return cls._CHOICES.value[action_key]
        except KeyError:
            raise ValueError('Action with key "{}" does not exists'.format(action_key))

    @classmethod
    def get_action_title(cls, action_key):

        if action_key.startswith('added'):
            return cls._TITLES.value[cls.ADDED_ACTION_TITLE.value]
        elif action_key.startswith('updated'):
            return cls._TITLES.value[cls.UPDATED_ACTION_TITLE.value]
        elif action_key.startswith('deleted'):
            return cls._TITLES.value[cls.DELETED_ACTION_TITLE.value]
        else:

            try:
                return cls._TITLES.value[action_key]
            except KeyError:
                raise ValueError('Unregisted action key "{}".'.format(action_key))
