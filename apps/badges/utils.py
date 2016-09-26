
from apps.polls.models import Poll


def check_badge_voter(user):

    count_votes = user.votes.count()

    if count_votes > 0:
        return True
    return False


def check_badge_electorate(user):

    count_votes = user.votes.count()

    total_count_polls = Poll._default_manager.count()

    half_total_count_polls = total_count_polls / 2

    if count_votes > half_total_count_polls:
        return True
    return False


def check_badge_vox_populi(user):

    count_votes = user.votes.count()

    total_count_polls = Poll._default_manager.count()

    if total_count_polls > 0 and count_votes == total_count_polls:
        return True
    return False


BADGES_CHECKERS = {
    'Voter': check_badge_voter,
    'Electorate': check_badge_electorate,
    'Vox Populi': check_badge_vox_populi,
}
