
from django.utils.translation import ugettext_lazy as _


NEW_MESSAGE = 'NEW_MESSAGE'
NEW_COMMENT = 'NEW_COMMENT'
CHANGING_REPUTATION = 'CHANGING_REPUTATION'
CREATED_OBJECT = 'CREATED_OBJECT'
UPDATED_OBJECT = 'UPDATED_OBJECT'
DELETED_OBJECT = 'DELETED_OBJECT'
CREATED_USER = 'CREATED_USER'
UPDATED_USER = 'UPDATED_USER'
UPDATED_PROFILE = 'UPDATED_PROFILE'
UPDATED_DIARY = 'UPDATED_DIARY'
DELETED_USER = 'DELETED_USER'
EARNED_BADGE = 'EARNED_BADGE'
LOST_BADGE = 'LOST_BADGE'

CHOICES_EVENT = (
    (NEW_MESSAGE, _('New message')),
    (NEW_COMMENT, _('New comment')),
    (CHANGING_REPUTATION, _('Changing reputation')),
    (CREATED_OBJECT, _('Created object')),
    (UPDATED_OBJECT, _('Updated object')),
    (DELETED_OBJECT, _('Deleted object')),
    (CREATED_USER, _('Created user')),
    (UPDATED_USER, _('Updated user')),
    (UPDATED_PROFILE, _('Updated profile')),
    (UPDATED_DIARY, _('Updated diary')),
    (DELETED_USER, _('Deleted user')),
    (EARNED_BADGE, _('Earned badge')),
    (LOST_BADGE, _('Lost badge')),
)
