

from django.utils.translation import ugettext_lazy as _


def get_contents(model):
    return {
        model.CREATED_USER: _('Welcome a new user. Your succefully registered.'),
        model.UPDATED_USER: _('Your succefully updated data of your user.'),
        model.UPDATED_PROFILE: _('Your succefully updated your profile.'),
        model.UPDATED_DIARY: _('Your succefully updated your diarly.'),
        model.EARNED_BADGE: _('You earned badge "{}"'),
        model.LOST_BADGE: _('You lost badge "{}"'),
    }
