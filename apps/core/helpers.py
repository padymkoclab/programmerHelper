import collections

from django.contrib.auth.models import Group

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


def get_recipients_while_deleting(users_for_deleting, GroupModerators, *users):

    if users_for_deleting is None:
        a = list()
        a.append(GroupModerators)
        a.extend(users)
        return a

    alive_recipients = GroupModerators.user_set.exclude(pk__in=[i.pk for i in users_for_deleting])
    alive_recipients = set(alive_recipients)

    for user in users:
        if user not in users_for_deleting:
            alive_recipients.add(user)

    return alive_recipients


def notify_badges(sender, instance, users_for_deleting=None):

    if sender in [
        Poll, Vote, Comment, Article, Mark, Question, Answer, Post, Topic,
        Snippet, Opinion, Reply, Solution, Visit, User, Profile, Diary
    ]:

        if users_for_deleting is None:
            users_for_deleting = ()

        users_lost_badges, users_earned_badges = check_badges_for_instance(instance, users_for_deleting)

        for user, badges in users_lost_badges.items():

            if user in users_for_deleting:
                continue

            for badge in badges:

                notify.send(
                    sender,
                    actor=user,
                    target=badge,
                    action=Actions.LOST_BADGE.value,
                    action_target=None,
                    level=Notification.SUCCESS,
                    recipient=user,
                )

        for user, badges in users_earned_badges.items():

            if user in users_for_deleting:
                continue

            for badge in badges:

                notify.send(
                    sender,
                    actor=user,
                    target=badge,
                    action=Actions.EARNED_BADGE.value,
                    action_target=None,
                    level=Notification.SUCCESS,
                    recipient=user,
                )


def check_badges_for_instance(instance, users_for_deleting):
    """ """

    users_lost_badges = collections.defaultdict(set)
    users_earned_badges = users_lost_badges.copy()

    if isinstance(instance, Vote):

        user = instance.user

        if user in users_for_deleting:
            return users_lost_badges, users_earned_badges

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

        if user in users_for_deleting:
            return users_lost_badges, users_earned_badges

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

        if user in users_for_deleting:
            return users_lost_badges, users_earned_badges

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

        if user in users_for_deleting:
            return users_lost_badges, users_earned_badges

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

        if user in users_for_deleting:
            return users_lost_badges, users_earned_badges

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

        if user in users_for_deleting:
            return users_lost_badges, users_earned_badges

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

        if user in users_for_deleting:
            return users_lost_badges, users_earned_badges

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

        if user in users_for_deleting:
            return users_lost_badges, users_earned_badges

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

        if user in users_for_deleting:
            return users_lost_badges, users_earned_badges

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.CRITIC_BRONZE, users_lost_badges, users_earned_badges, Opinion
        )

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.SUPPORTER_BRONZE, users_lost_badges, users_earned_badges, Opinion
        )

    elif isinstance(instance, Reply):

        user = instance.user

        if user in users_for_deleting:
            return users_lost_badges, users_earned_badges

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

        if user in users_for_deleting:
            return users_lost_badges, users_earned_badges

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

        if user in users_for_deleting:
            return users_lost_badges, users_earned_badges

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.FREQUENT_RECORDER_BRONZE, users_lost_badges, users_earned_badges, Diary
        )

    elif isinstance(instance, Profile):

        user = instance.user

        if user in users_for_deleting:
            return users_lost_badges, users_earned_badges

        users_lost_badges, users_earned_badges = update_badges_and_return_result(
            user, Badges.Badge.AUTOBIOGRAPHER_BRONZE, users_lost_badges, users_earned_badges, Profile
        )

    if isinstance(instance, Poll):

        users_pks = Vote._default_manager.filter(poll=instance).values('user')
        users = User._default_manager.filter(pk__in=users_pks)

        for user in users:

            if user in users_for_deleting:
                continue

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

        if user in users_for_deleting:
            return users_lost_badges, users_earned_badges

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


def notify_activity(sender, instance, action, users_for_deleting=None):

    if sender in [
        User, Vote, Solution, Snippet, Question, Answer, Profile, Diary,
        Article, Mark, Reply, Comment, Opinion, Post, Topic,
    ]:

        GroupModerators = Group.objects.get(name='moderators')

        if action == 'created':

            # profile will be created automaticaly
            if sender == Profile:
                return

            if sender == Diary:

                actor = instance.user
                action_target = None
                action = Actions.ACTIVATED_DIARY.value
                target = None
                recipient = (GroupModerators, instance.user)

            elif sender in [Vote, Opinion, Comment, Mark, Answer, Reply, Post]:

                actor = instance.user
                action_target = instance

                if sender == Opinion:
                    action = Actions.ADDED_OPINION.value
                    target = instance.content_object
                    recipient = (GroupModerators, instance.content_object.user)
                elif sender == Vote:
                    action = Actions.ADDED_VOTE.value
                    target = instance.poll
                    recipient = GroupModerators
                elif sender == Comment:
                    action = Actions.ADDED_COMMENT.value
                    target = instance.content_object
                    recipient = (GroupModerators, instance.content_object.user)
                elif sender == Mark:
                    action = Actions.ADDED_MARK.value
                    target = instance.article
                    recipient = (GroupModerators, instance.article.user)
                elif sender == Answer:
                    action = Actions.ADDED_ANSWER.value
                    target = instance.question
                    recipient = (GroupModerators, instance.question.user)
                elif sender == Reply:
                    action = Actions.ADDED_REPLY.value
                    target = instance.book
                    recipient = GroupModerators
                elif sender == Post:
                    action = Actions.ADDED_POST.value
                    target = instance.topic
                    recipient = (GroupModerators, instance.topic.user)

            elif sender in [Solution, Snippet, Question, Article, Topic]:
                target = instance
                actor = instance.user
                recipient = GroupModerators
                action_target = None

                if sender == Solution:
                    action = Actions.ADDED_SOLUTION.value
                elif sender == Question:
                    action = Actions.ADDED_QUESTION.value
                elif sender == Snippet:
                    action = Actions.ADDED_SNIPPET.value
                elif sender == Article:
                    action = Actions.ADDED_ARTICLE.value
                elif sender == Topic:
                    action = Actions.ADDED_TOPIC.value

            elif sender == User:
                action = Actions.REGISTRED_USER.value
                target = None
                action_target = None
                actor = instance
                recipient = (instance, GroupModerators)

            notify.send(
                sender,
                actor=actor,
                target=target,
                recipient=recipient,
                action=action,
                action_target=action_target,
                level=Notification.SUCCESS,
            )

        elif action == 'updated' and instance.is_changed() is True:

            if sender in [Vote, Opinion, Comment, Mark, Answer, Reply, Post, Profile, Diary]:

                actor = instance.user
                action_target = instance

                if sender == Opinion:
                    target = instance.content_object
                    action = Actions.UPDATED_OPINION.value
                    recipient = (GroupModerators, instance.content_object.user)
                elif sender == Vote:
                    target = instance.poll
                    action = Actions.UPDATED_VOTE.value
                    recipient = GroupModerators
                elif sender == Comment:
                    target = instance.content_object
                    action = Actions.UPDATED_COMMENT.value
                    recipient = (GroupModerators, instance.content_object.user)
                elif sender == Mark:
                    target = instance.article
                    action = Actions.UPDATED_MARK.value
                    recipient = (GroupModerators, instance.article.user)
                elif sender == Answer:
                    target = instance.question
                    action = Actions.UPDATED_ANSWER.value
                    recipient = (GroupModerators, instance.question.user)
                elif sender == Reply:
                    target = instance.book
                    action = Actions.UPDATED_REPLY.value
                    recipient = GroupModerators
                elif sender == Post:
                    target = instance.topic
                    action = Actions.UPDATED_POST.value
                    recipient = (GroupModerators, instance.topic.user)
                elif sender == Diary:
                    raise
                    # action = Actions.ACTIVATED_DIARY.value
                    target = None
                    action = Actions.UPDATED_DIARY.value
                    recipient = instance.user
                elif sender == Profile:
                    target = None
                    action = Actions.UPDATED_PROFILE.value
                    recipient = instance.user

            elif sender in [Solution, Snippet, Question, Article, Topic]:
                action_target = None
                target = instance
                actor = instance.user
                recipient = GroupModerators

                if sender == Solution:
                    action = Actions.UPDATED_SOLUTION.value
                elif sender == Question:
                    action = Actions.UPDATED_QUESTION.value
                elif sender == Snippet:
                    action = Actions.UPDATED_SNIPPET.value
                elif sender == Article:
                    action = Actions.UPDATED_ARTICLE.value
                elif sender == Topic:
                    action = Actions.UPDATED_TOPIC.value

            elif sender == User:
                action = Actions.UPDATED_USER.value
                action_target = None
                target = None
                actor = instance
                recipient = instance

            notify.send(
                sender,
                actor=actor,
                target=target,
                action=action,
                action_target=action_target,
                level=Notification.SUCCESS,
                recipient=recipient,
            )

        elif action == 'deleted':

            if sender in [
                User, Solution, Snippet, Question, Answer, Article,
                Mark, Reply, Comment, Opinion, Post, Topic, Vote,
            ]:

                actor = instance if sender == User else instance.user

                if users_for_deleting and actor in users_for_deleting:
                    actor = actor.get_full_name()

                if sender == Mark:
                    target = instance.article
                    action_target = instance
                    action = Actions.DELETED_MARK.value
                    recipient = get_recipients_while_deleting(
                        users_for_deleting, GroupModerators, instance.article.user
                    )
                elif sender == Answer:
                    target = instance.question
                    action_target = instance
                    action = Actions.DELETED_ANSWER.value
                    recipient = get_recipients_while_deleting(
                        users_for_deleting, GroupModerators, instance.question.user
                    )
                elif sender == Vote:
                    target = instance.poll
                    action_target = instance
                    action = Actions.DELETED_VOTE.value
                    recipient = get_recipients_while_deleting(users_for_deleting, GroupModerators)
                elif sender == Reply:
                    target = instance.book
                    action_target = instance
                    action = Actions.DELETED_REPLY.value
                    recipient = get_recipients_while_deleting(users_for_deleting, GroupModerators)
                elif sender == Post:
                    target = instance.topic
                    action_target = instance
                    action = Actions.DELETED_POST.value
                    recipient = get_recipients_while_deleting(users_for_deleting, GroupModerators, instance.topic.user)
                elif sender == Opinion:
                    target = instance.content_object
                    action_target = instance
                    action = Actions.DELETED_OPINION.value
                    recipient = get_recipients_while_deleting(
                        users_for_deleting, GroupModerators, instance.content_object.user
                    )
                elif sender == Comment:
                    target = instance.content_object
                    action_target = instance
                    action = Actions.DELETED_COMMENT.value
                    recipient = get_recipients_while_deleting(
                        users_for_deleting, GroupModerators, instance.content_object.user
                    )
                elif sender in (Solution, Snippet, Question, Article, Topic):
                    target = instance
                    action_target = None
                    recipient = get_recipients_while_deleting(users_for_deleting, GroupModerators, instance.user)

                    if sender == Solution:
                        action = Actions.DELETED_SOLUTION.value
                    elif sender == Question:
                        action = Actions.DELETED_QUESTION.value
                    elif sender == Snippet:
                        action = Actions.DELETED_SNIPPET.value
                    elif sender == Article:
                        action = Actions.DELETED_ARTICLE.value
                    elif sender == Topic:
                        action = Actions.DELETED_TOPIC.value

                elif sender == User:
                    target = None
                    action_target = None
                    action = Actions.DELETED_USER.value
                    recipient = get_recipients_while_deleting(users_for_deleting, GroupModerators)

                if recipient:
                    notify.send(
                        sender,
                        actor=actor,
                        target=target,
                        action=action,
                        action_target=action_target,
                        level=Notification.SUCCESS,
                        recipient=recipient,
                    )


def notify_reputation(sender, instance, action, users_for_deleting, update_fields=None):

    if sender in (Vote, Opinion, Mark):

        is_changed = False

        if sender == Vote:

            recipient = instance.user

            if users_for_deleting is not None and recipient in users_for_deleting:
                return

            target = instance.poll

            if action == 'created':
                action = Actions.REPUTATION_PARTICIPATE_IN_POLL.value
                is_changed = True
            elif action == 'deleted':
                action = Actions.REPUTATION_UNDO_PARTICIPATE_IN_POLL.value
                is_changed = True

        elif sender == Opinion:

            recipient = instance.content_object.user

            if users_for_deleting is not None and recipient in users_for_deleting:
                return

            target = instance.content_object

            if action == 'created':

                if instance.is_useful is True:
                    action = Actions.REPUTATION_UPVOTE_OPINION.value
                    is_changed = True
                elif instance.is_useful is False:
                    action = Actions.REPUTATION_DOWNVOTE_OPINION.value
                    is_changed = True

            elif action == 'updated' and instance.is_changed() is True:

                if instance.is_useful is True:
                    action = Actions.REPUTATION_CHANGED_TO_DOWNVOTE_OPINION.value
                    is_changed = True
                elif instance.is_useful is False:
                    action = Actions.REPUTATION_CHANGED_TO_UPVOTE_OPINION.value
                    is_changed = True

            elif action == 'deleted':

                if instance.is_useful is True:
                    action = Actions.REPUTATION_LOSE_UPVOTE_OPINION.value
                    is_changed = True
                elif instance.is_useful is False:
                    action = Actions.REPUTATION_LOSE_DOWNVOTE_OPINION.value
                    is_changed = True

        elif sender == Mark:

            recipient = instance.article.user

            if users_for_deleting is not None and recipient in users_for_deleting:
                return

            if action == 'created':
                pass
            elif action == 'updated':
                pass
            elif action == 'deleted':
                pass

            target = instance.article

        if is_changed is False:
            return

        value = Actions.get_reputation_deviation(action, target)

        recipient.reputation += int(value)
        recipient.full_clean()
        recipient.save()

        notify.send(
            sender,
            actor=None,
            target=target,
            action=action,
            action_target=None,
            level=Notification.SUCCESS,
            recipient=recipient,
        )
