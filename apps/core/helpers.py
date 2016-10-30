
import collections

from apps.polls.models import Poll, Vote
from apps.comments.models import Comment
from apps.articles.models import Article, Mark
from apps.questions.models import Question, Answer
from apps.forums.models import Post, Topic
from apps.snippets.models import Snippet
from apps.opinions.models import Opinion
from apps.library.models import Reply
from apps.solutions.models import Solution
from apps.visits.models import Attendance, Visit
from apps.users.models import User, Profile
from apps.diaries.models import Diary

from apps.badges.constants import Badges
from apps.badges.models import Badge, EarnedBadge

from apps.notifications.models import Notification
from apps.notifications.signals import notify
from apps.notifications.constants import Actions


def check_badges_for_instance_and_notify(sender, instance):

    if sender in [
        Poll, Vote, Comment, Article, Mark, Question, Answer, Post, Topic,
        Snippet, Opinion, Reply, Solution, Visit, User, Profile, Diary
    ]:

        return

        users_lost_badges, users_earned_badges = check_badges_for_instance(instance)

        for user, badges in users_lost_badges.items():

            for badge in badges:

                notify.send(
                    sender,
                    user=user,
                    target=badge,
                    action=Actions.DELETED_BADGE.value,
                    action_target=None,
                    level=Notification.INFO,
                )

        for user, badges in users_earned_badges.items():

            for badge in badges:

                notify.send(
                    sender,
                    user=user,
                    target=badge,
                    action=Actions.ADDED_BADGE.value,
                    action_target=None,
                    level=Notification.INFO,
                )


def check_badges_for_instance(instance):
    """ """

    users_lost_badges = collections.defaultdict(set)
    users_earned_badges = users_lost_badges.copy()

    if isinstance(instance, Vote):

        user = instance.user

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.VOTER_BRONZE, users_lost_badges, users_earned_badges, Vote
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.VOTER_SILVER, users_lost_badges, users_earned_badges, Vote
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.VOTER_GOLD, users_lost_badges, users_earned_badges, Poll, Vote
        )

    elif isinstance(instance, Comment):

        user = instance.user

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.COMMENTATOR_BRONZE, users_lost_badges, users_earned_badges, Comment
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.COMMENTATOR_SILVER, users_lost_badges, users_earned_badges, Comment
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.COMMENTATOR_GOLD, users_lost_badges, users_earned_badges, Comment
        )

    elif isinstance(instance, (Mark, Article)):

        user = instance.user if isinstance(instance, Article) else instance.article.user

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.PUBLICIST_BRONZE, users_lost_badges, users_earned_badges, Article
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.PUBLICIST_SILVER, users_lost_badges, users_earned_badges, Article
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.PUBLICIST_GOLD, users_lost_badges, users_earned_badges, Article
        )

    elif isinstance(instance, Solution):

        user = instance.user

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.INVENTOR_BRONZE, users_lost_badges, users_earned_badges, Solution
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.INVENTOR_SILVER, users_lost_badges, users_earned_badges, Solution
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.INVENTOR_GOLD, users_lost_badges, users_earned_badges, Solution
        )

    elif isinstance(instance, Snippet):

        user = instance.user

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.CODER_BRONZE, users_lost_badges, users_earned_badges, Snippet
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.CODER_SILVER, users_lost_badges, users_earned_badges, Snippet
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.CODER_GOLD, users_lost_badges, users_earned_badges, Snippet
        )

    elif isinstance(instance, Question):

        user = instance.user

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.QUESTIONER_BRONZE, users_lost_badges, users_earned_badges, Question
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.QUESTIONER_SILVER, users_lost_badges, users_earned_badges, Question
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.QUESTIONER_GOLD, users_lost_badges, users_earned_badges, Question
        )

    elif isinstance(instance, Answer):

        user = instance.user

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.TEACHER_BRONZE, users_lost_badges, users_earned_badges, Answer
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.ENLIGHTENED_SILVER, users_lost_badges, users_earned_badges, Answer
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.GURU_GOLD, users_lost_badges, users_earned_badges, Answer
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.SELF_LEARNER_BRONZE, users_lost_badges, users_earned_badges, Answer
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.SCHOOLAR_BRONZE, users_lost_badges, users_earned_badges, Answer
        )

    elif isinstance(instance, (Topic, Post)):

        user = instance.user

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.INTERLOCUTOR_BRONZE, users_lost_badges, users_earned_badges, Post
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.INITIALIZER_CONVERSATION_BRONZE, users_lost_badges, users_earned_badges, Topic
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.FORUMER_SILVER, users_lost_badges, users_earned_badges, Topic, Post
        )

    elif isinstance(instance, Opinion):

        user = instance.user

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.CRITIC_BRONZE, users_lost_badges, users_earned_badges, Opinion
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.SUPPORTER_BRONZE, users_lost_badges, users_earned_badges, Opinion
        )

    elif isinstance(instance, Reply):

        user = instance.user

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.READER_BRONZE, users_lost_badges, users_earned_badges, Reply
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.BOOKLOVER_SILVER, users_lost_badges, users_earned_badges, Reply
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.BIBLIOPHILE_GOLD, users_lost_badges, users_earned_badges, Reply
        )

    elif isinstance(instance, Visit):

        user = instance.user

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.YEARLING_BRONZE, users_lost_badges, users_earned_badges, Visit
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.ENTHUSIAST_BRONZE, users_lost_badges, users_earned_badges, Attendance
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.FANATIC_SILVER, users_lost_badges, users_earned_badges, Attendance
        )

    elif isinstance(instance, Diary):

        user = instance.user

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.FREQUENT_RECORDER_BRONZE, users_lost_badges, users_earned_badges, Diary
        )

    elif isinstance(instance, Profile):

        user = instance.user

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.AUTOBIOGRAPHER_BRONZE, users_lost_badges, users_earned_badges, Profile
        )

    if isinstance(instance, Poll):

        users_pks = Vote._default_manager.filter(poll=instance).values('user')
        users = User._default_manager.filter(pk__in=users_pks)

        for user in users:

            users_lost_badges, users_earned_badges = update_badges_and_return_result(
                user, Badges.Badge.VOTER_BRONZE, users_lost_badges, users_earned_badges, Vote
            )

            users_lost_badges, users_earned_badges = update_badges_and_return_result(
                user, Badges.Badge.VOTER_SILVER, users_lost_badges, users_earned_badges, Vote
            )

            users_lost_badges, users_earned_badges = update_badges_and_return_result(
                user, Badges.Badge.VOTER_GOLD, users_lost_badges, users_earned_badges, Poll, Vote
            )

    else:

        if isinstance(instance, User):
            user = instance

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.EPIC_SILVER, users_lost_badges, users_earned_badges
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.LEGENDARY_GOLD, users_lost_badges, users_earned_badges
        )

    return users_lost_badges, users_earned_badges


def check_badge_for_user(user, badge_const, *checker_args):

    checker = Badges.checkers[badge_const]
    return checker(user, *checker_args)


def update_badges_and_return_result(user, badge_const, users_lost_badges, users_earned_badges, *checker_args):

    badge = Badge.objects.get(name=badge_const.value)

    must_earn_badge = check_badge_for_user(user, badge_const, *checker_args)

    if must_earn_badge is False and Badge.objects.has_badge(badge, user) is True:

        EarnedBadge.objects.delete_if_exists(user, badge)

        users_lost_badges[user].add(badge)

    if must_earn_badge is True and Badge.objects.has_badge(badge, user) is False:

        earned_badge = EarnedBadge(user=user, badge=badge)
        earned_badge.full_clean()
        earned_badge.save()

        users_earned_badges[user].add(badge)

    return users_lost_badges, users_earned_badges


def make_notification(sender, instance, action):

    if sender in [
        User, Vote, Solution, Snippet, Question, Answer, Profile, Diary,
        Article, Mark, Reply, Comment, Opinion, Post, Topic
    ]:

        if action == 'created':

            if sender in [Diary, Profile]:

                return

            elif sender in [Vote, Opinion, Comment, Mark, Answer, Reply, Post]:

                user = instance.user
                action_target = instance

                if sender == Vote:
                    action = Actions.ADDED_VOTE.value
                    target = instance.poll
                elif sender == Opinion:
                    action = Actions.ADDED_OPINION.value
                    target = instance.content_object
                elif sender == Comment:
                    action = Actions.ADDED_COMMENT.value
                    target = instance.content_object
                elif sender == Mark:
                    action = Actions.ADDED_MARK.value
                    target = instance.article
                elif sender == Answer:
                    action = Actions.ADDED_ANSWER.value
                    target = instance.question
                elif sender == Reply:
                    action = Actions.ADDED_REPLY.value
                    target = instance.book
                elif sender == Post:
                    action = Actions.ADDED_POST.value
                    target = instance.topic

            elif sender in [Solution, Snippet, Question, Article, Topic]:
                action = Actions.ADDED_OBJECT.value
                target = instance
                user = instance.user
                action_target = None

            elif sender == User:
                action = Actions.ADDED_USER.value
                target = None
                action_target = None
                user = instance

            notify.send(
                sender,
                user=user,
                target=target,
                action=action,
                action_target=action_target,
                level=Notification.SUCCESS,
            )

        elif action == 'updated':

            if sender in [Vote, Opinion, Comment, Mark, Answer, Reply, Post, Profile, Diary]:

                user = instance.user
                action_target = instance

                if sender == Vote:
                    target = instance.poll
                    action = Actions.UPDATED_VOTE.value
                elif sender == Opinion:
                    target = instance.content_object
                    action = Actions.UPDATED_OPINION.value
                elif sender == Comment:
                    target = instance.content_object
                    action = Actions.UPDATED_COMMENT.value
                elif sender == Mark:
                    target = instance.article
                    action = Actions.UPDATED_MARK.value
                elif sender == Answer:
                    target = instance.question
                    action = Actions.UPDATED_ANSWER.value
                elif sender == Reply:
                    target = instance.book
                    action = Actions.UPDATED_REPLY.value
                elif sender == Post:
                    target = instance.topic
                    action = Actions.UPDATED_POST.value
                elif sender == Diary:
                    target = None
                    action = Actions.UPDATED_DIARY.value
                elif sender == Profile:
                    target = None
                    action = Actions.UPDATED_PROFILE.value

            elif sender in [Solution, Snippet, Question, Article, Topic]:
                action = Actions.UPDATED_OBJECT.value
                action_target = None
                target = instance
                user = instance.user

            elif sender == User:
                action = Actions.UPDATED_USER.value
                action_target = None
                target = None
                user = instance

            notify.send(
                sender,
                user=user,
                target=target,
                action=action,
                action_target=action_target,
                level=Notification.SUCCESS,
            )

        elif action == 'deleted':

            if sender in [
                User, Vote, Solution, Snippet, Question, Answer, Article,
                Mark, Reply, Comment, Opinion, Post, Topic
            ]:

                user = instance if sender == User else instance.user

                if sender == Vote:
                    target = instance.poll
                    action_target = instance
                    action = Actions.DELETED_VOTE.value
                elif sender == Mark:
                    target = instance.article
                    action_target = instance
                    action = Actions.DELETED_MARK.value
                elif sender == Answer:
                    target = instance.question
                    action_target = instance
                    action = Actions.DELETED_ANSWER.value
                elif sender == Reply:
                    target = instance.book
                    action_target = instance
                    action = Actions.DELETED_REPLY.value
                elif sender == Post:
                    target = instance.topic
                    action_target = instance
                    action = Actions.DELETED_POST.value
                elif sender == User:
                    target = None
                    action_target = None
                    action = Actions.DELETED_USER.value
                elif sender == Solution:
                    target = instance
                    action_target = None
                    action = Actions.DELETED_OBJECT.value
                elif sender == Snippet:
                    target = instance
                    action_target = None
                    action = Actions.DELETED_OBJECT.value
                elif sender == Question:
                    target = instance
                    action_target = None
                    action = Actions.DELETED_OBJECT.value
                elif sender == Article:
                    target = instance
                    action_target = None
                    action = Actions.DELETED_OBJECT.value
                elif sender == Topic:
                    target = instance
                    action_target = None
                    action = Actions.DELETED_OBJECT.value
                elif sender == Opinion:
                    target = instance.content_object
                    action_target = instance
                    action = Actions.DELETED_OPINION.value
                elif sender == Comment:
                    target = instance.content_object
                    action_target = instance
                    action = Actions.DELETED_COMMENT.value

                notify.send(
                    sender,
                    user=user,
                    target=target,
                    action=action,
                    action_target=action_target,
                    level=Notification.SUCCESS,
                )
