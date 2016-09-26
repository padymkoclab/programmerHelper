
from apps.polls.models import Poll


def check_badge_frequent_recorder(user):

    total_size = user.diary.get_total_size()

    if total_size >= 250000:
        return True
    return False


def check_badge_voter(user):

    count_votes = user.get_count_votes()

    if count_votes > 0:
        return True
    return False


def check_badge_electorate(user):

    count_votes = user.get_count_votes()

    total_count_polls = Poll._default_manager.count()

    half_total_count_polls = total_count_polls / 2

    if count_votes > half_total_count_polls:
        return True
    return False


def check_badge_vox_populi(user):

    count_votes = user.get_count_votes()

    total_count_polls = Poll._default_manager.count()

    if total_count_polls > 0 and count_votes == total_count_polls:
        return True
    return False


BADGES_CHECKERS = {
    'Voter': check_badge_voter,
    'Electorate': check_badge_electorate,
    'Vox Populi': check_badge_vox_populi,
    'Frequent recorder': check_badge_frequent_recorder,
}
