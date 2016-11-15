
import itertools

from dateutil.relativedelta import relativedelta

from .utils import check_boolean_return


@check_boolean_return
def check_badge_commentator_bronze(user, comment_model):
    """Has at least 10 comments."""

    return comment_model._default_manager.filter(user=user).count() >= 10


@check_boolean_return
def check_badge_commentator_silver(user, comment_model):
    """Has at least 50 comments."""

    return comment_model._default_manager.filter(user=user).count() >= 50


@check_boolean_return
def check_badge_commentator_gold(user, comment_model):
    """Has at least 100 comments."""

    return comment_model._default_manager.filter(user=user).count() >= 100


@check_boolean_return
def check_badge_voter_bronze(user, vote_model):
    """Has a vote in a poll."""

    return vote_model._default_manager.filter(user=user).exists()


@check_boolean_return
def check_badge_voter_silver(user, vote_model):
    """Has a vote in more than half count of all polls."""

    return vote_model._default_manager.is_active_voter(user)


@check_boolean_return
def check_badge_voter_gold(user, poll_model, vote_model):
    """Has a vote in all polls."""

    count_polls = poll_model._default_manager.count()

    return vote_model._default_manager.filter(user__pk=user.pk).count() == count_polls


@check_boolean_return
def check_badge_publicist_bronze(user, article_model):
    """Has an article with rating more 0 and at least 100 views."""

    qs = article_model._default_manager.filter(user=user, count_views__gte=100)

    if qs.exists():
        return qs.objects_with_rating().filter(rating__gt=0).exists()

    return False


@check_boolean_return
def check_badge_publicist_silver(user, article_model):
    """Has an article with rating at least 10 and and at least 500 views."""

    qs = article_model._default_manager.filter(user=user, count_views__gte=500)

    if qs.exists():
        return qs.objects_with_rating().filter(rating__gte=10).exists()

    return False


@check_boolean_return
def check_badge_publicist_gold(user, article_model):
    """Has an article with rating at least 50 and at least 1000 views."""

    qs = article_model._default_manager.filter(user=user, count_views__gte=1000)

    if qs.exists():
        return qs.objects_with_rating().filter(rating__gte=50).exists()

    return False


@check_boolean_return
def check_badge_coder_bronze(user, snippet_model):
    """Has a snippet with rating more 0 and at least 100 views."""

    qs = snippet_model._default_manager.filter(user=user, count_views__gte=100)

    if qs.exists():
        return qs.objects_with_rating().filter(rating__gt=0).exists()

    return False


@check_boolean_return
def check_badge_coder_silver(user, snippet_model):
    """Has a snippet with rating at least 10 and at least 500 views."""

    qs = snippet_model._default_manager.filter(user=user, count_views__gte=500)

    if qs.exists():
        return qs.objects_with_rating().filter(rating__gte=10).exists()

    return False


@check_boolean_return
def check_badge_coder_gold(user, snippet_model):
    """Has a snippet with rating at least 50 and at least 1000 views."""

    qs = snippet_model._default_manager.filter(user=user, count_views__gte=1000)

    if qs.exists():
        return qs.objects_with_rating().filter(rating__gte=50).exists()

    return False


@check_boolean_return
def check_badge_inventor_bronze(user, solution_model):
    """Has a solution with rating more 0 and at least 100 views."""

    qs = solution_model._default_manager.filter(user=user, count_views__gte=100)

    if qs.exists():
        return qs.objects_with_rating().filter(rating__gt=0).exists()

    return False


@check_boolean_return
def check_badge_inventor_silver(user, solution_model):
    """Has a solution with rating at least 10 and at least 500 views."""

    qs = solution_model._default_manager.filter(user=user, count_views__gte=500)

    if qs.exists():
        return qs.objects_with_rating().filter(rating__gte=10).exists()

    return False


@check_boolean_return
def check_badge_inventor_gold(user, solution_model):
    """Has a solution with rating at least 50 and at least 1000 views."""

    qs = solution_model._default_manager.filter(user=user, count_views__gte=1000)

    if qs.exists():
        return qs.objects_with_rating().filter(rating__gte=50).exists()

    return False


@check_boolean_return
def check_badge_questioner_bronze(user, question_model):
    """Has a question with rating more 0 and at least 100 views."""

    qs = question_model._default_manager.filter(user=user, count_views__gte=100)

    if qs.exists():
        return qs.objects_with_rating().filter(rating__gt=0).exists()

    return False


@check_boolean_return
def check_badge_questioner_silver(user, question_model):
    """Has a question with rating at least 10 and at least 500 views."""

    qs = question_model._default_manager.filter(user=user, count_views__gte=500)

    if qs.exists():
        return qs.objects_with_rating().filter(rating__gte=10).exists()

    return False


@check_boolean_return
def check_badge_questioner_gold(user, question_model):
    """Has a question with rating at least 50 and at least 1000 views."""

    qs = question_model._default_manager.filter(user=user, count_views__gte=1000)

    if qs.exists():
        return qs.objects_with_rating().filter(rating__gte=50).exists()

    return False


@check_boolean_return
def check_badge_teacher_bronze(user, answer_model):
    """Has an answer with rating more 0."""

    qs = answer_model._default_manager.filter(user=user)

    if qs.exists():
        return qs.objects_with_rating().filter(rating__gt=0).exists()

    return False


@check_boolean_return
def check_badge_enlightened_silver(user, answer_model):
    """Has an answer with rating at least 10."""

    qs = answer_model._default_manager.filter(user=user)

    if qs.exists():
        return qs.objects_with_rating().filter(rating__gte=10).exists()

    return False


@check_boolean_return
def check_badge_guru_gold(user, answer_model):
    """Has an answer with rating at least 50."""

    qs = answer_model._default_manager.filter(user=user)

    if qs.exists():
        return qs.objects_with_rating().filter(rating__gte=50).exists()

    return False


@check_boolean_return
def check_badge_self_learner_bronze(user, answer_model):
    """Gave an answer on your own question with rating at least 3."""

    qs = answer_model._default_manager.filter(user=user, question__user=user)

    if qs.exists():
        return qs.objects_with_rating().filter(rating__gt=3).exists()

    return False


@check_boolean_return
def check_badge_schoolar_bronze(user, answer_model):
    """Asked a question and accept an answer."""

    return answer_model._default_manager.filter(question__user=user, is_accepted=True).exists()


@check_boolean_return
def check_badge_interlocutor_bronze(user, post_model):
    """Has a post on a forum."""

    return post_model._default_manager.filter(user=user).exists()


@check_boolean_return
def check_badge_initializer_conversation_bronze(user, topic_model):
    """Has a topic on a forum."""

    return topic_model._default_manager.filter(user=user).exists()


@check_boolean_return
def check_badge_forumer_silver(user, topic_model, post_model):
    """Has at least 10 topics and at least 50 posts on forums."""

    count_topics_user = topic_model._default_manager.filter(user=user).count()
    count_posts_user = post_model._default_manager.filter(user=user).count()

    return count_topics_user >= 10 and count_posts_user >= 50


@check_boolean_return
def check_badge_enthusiast_bronze(user, attendance_model):
    """Visit the site each day for 30 consecutive days."""

    qs = attendance_model._default_manager.filter(users=user)

    dates = tuple(qs.values_list('date', flat=True))

    pairs_neighboring_dates = zip(dates[0:-1], dates[1:])

    diffrence_days = (map(lambda i: (i[0] - i[1]).days, pairs_neighboring_dates))

    perionds_consecutive_days = (len(tuple(i)) for k, i in itertools.groupby(diffrence_days) if k == 1)

    return bool(tuple(filter(lambda i: i > 29, perionds_consecutive_days)))


@check_boolean_return
def check_badge_frequent_recorder_bronze(user, diary_model):
    """Has at least 250000 characters in a diary."""

    diary = diary_model._default_manager.get(user=user)
    return diary.get_total_size() >= 250000


@check_boolean_return
def check_badge_fanatic_silver(user, attendance_model):
    """Visit the site each day for 100 consecutive days."""

    qs = attendance_model._default_manager.filter(users=user)

    dates = tuple(qs.values_list('date', flat=True))

    pairs_neighboring_dates = zip(dates[0:-1], dates[1:])

    diffrence_days = (map(lambda i: (i[0] - i[1]).days, pairs_neighboring_dates))

    perionds_consecutive_days = [len(tuple(i)) for k, i in itertools.groupby(diffrence_days) if k == 1]

    return bool(tuple(filter(lambda i: i > 99, perionds_consecutive_days)))


@check_boolean_return
def check_badge_epic_silver(user):
    """Reputation is at least 1000."""

    return user.reputation >= 1000


@check_boolean_return
def check_badge_legendary_gold(user):
    """Reputation is at least 10000."""

    return user.reputation >= 10000


@check_boolean_return
def check_badge_yearling_bronze(user, visit_model):
    """More 1 year as registered."""

    date_latest_visit = visit_model._default_manager.get(user=user).updated
    return date_latest_visit >= user.date_joined + relativedelta(years=1)


@check_boolean_return
def check_badge_autobiographer_bronze(user, profile_model):
    """Filled own profile at least 90%."""

    profile = profile_model._default_manager.get(user=user)
    return profile.get_percentage_filling() >= 90


@check_boolean_return
def check_badge_critic_bronze(user, opinion_model):
    """First down vote."""

    return opinion_model._default_manager.filter(user=user, is_useful=False).exists()


@check_boolean_return
def check_badge_supporter_bronze(user, opinion_model):
    """First up vote."""

    return opinion_model._default_manager.filter(user=user, is_useful=True).exists()


@check_boolean_return
def check_badge_outspoken_bronze(user):
    """Has 100 messages in a chat for a day."""

    return False


@check_boolean_return
def check_badge_talkative_bronze(user):
    """Has 500 messages in a chat for a day."""

    return False


@check_boolean_return
def check_badge_reader_bronze(user, reply_model):
    """Has reply about a book."""

    return reply_model._default_manager.filter(user=user).exists()


@check_boolean_return
def check_badge_booklover_silver(user, reply_model):
    """Has replies about at least 5 books."""

    return reply_model._default_manager.filter(user=user).count() >= 5


@check_boolean_return
def check_badge_bibliophile_gold(user, reply_model):
    """Has replies about at least 10 books."""

    return reply_model._default_manager.filter(user=user).count() >= 10
