

def check_badge_commentator_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_commentator_silver(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_commentator_gold(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_voter_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    vote_model = args[0]

    for user in users.iterator():

        if vote_model._default_manager.filter(user__pk=user.pk).exists():
            users_earned_badge.append(user)
        else:
            users_lost_badge.append(user)

    return users_lost_badge, users_earned_badge


def check_badge_voter_silver(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    vote_model = args[0]
    poll_model = args[1]

    count_polls = poll_model._default_manager.count()

    for user in users.iterator():

        count_votes_user = vote_model._default_manager.filter(user__pk=user.pk).count()

        if count_polls / 2 < count_votes_user:
            users_earned_badge.append(user)
        else:
            users_lost_badge.append(user)

    return users_lost_badge, users_earned_badge


def check_badge_voter_gold(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    vote_model = args[0]
    poll_model = args[1]

    count_polls = poll_model._default_manager.count()

    for user in users.iterator():

        if vote_model._default_manager.filter(user__pk=user.pk).count() == count_polls:
            users_earned_badge.append(user)
        else:
            users_lost_badge.append(user)

    return users_lost_badge, users_earned_badge


def check_badge_publicist_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_publicist_silver(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_publicist_gold(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_coder_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_coder_silver(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_coder_gold(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_inventor_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_inventor_silver(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_inventor_gold(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_questioner_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_questioner_silver(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_questioner_gold(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_teacher_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_enlightened_silver(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_guru_gold(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_self_learner_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_schoolar_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_interlocutor_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_initializer_conversation_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_forumer_silver(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_enthusiast_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_frequent_recorder_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_fanatic_silver(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_epic_silver(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_legendary_gold(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_yearling_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_autobiographer_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_critic_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_supporter_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_outspoken_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge


def check_badge_talkative_bronze(users, *args):
    """ """

    users_lost_badge, users_earned_badge = [], []

    return users_lost_badge, users_earned_badge

