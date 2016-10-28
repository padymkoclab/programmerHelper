
import uuid
import logging

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import pre_save, post_save, m2m_changed, pre_delete, post_delete
# from django.core.exceptions import ValidationError
# from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
# from django.conf import settings
# from django.contrib.auth import get_user_model

from apps.users.models import User, Profile
from apps.diaries.models import Diary
from apps.polls.models import Vote, Poll, Choice
from apps.snippets.models import Snippet
from apps.solutions.models import Solution
from apps.articles.models import Article, Mark
from apps.questions.models import Question, Answer
from apps.forums.models import Topic, Post
from apps.library.models import Reply
from apps.comments.models import Comment
from apps.opinions.models import Opinion
from apps.badges.models import Badge

from apps.notifications.signals import notify
from apps.notifications.models import Notification
from apps.notifications.constants import Actions


logger = logging.getLogger('django.development')


@receiver(post_save, dispatch_uid=uuid.uuid4)
def added_update_object(sender, instance, created, **kwargs):

    if sender in [
        User, Vote, Solution, Snippet, Question, Answer, Profile, Diary,
        Article, Mark, Reply, Comment, Opinion, Post, Topic
    ]:

        if sender in [Diary, Profile]:

            return

        if created is True:

            if sender in [Vote, Opinion, Comment, Mark, Answer, Reply, Post]:

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

        else:

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

    if sender in [Poll, Vote] and created is True:

        users_lost_badges, users_earned_badges = Badge.objects.check_badges_for_instance(instance)

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


@receiver(pre_delete, dispatch_uid=uuid.uuid4)
def deleted_object(sender, instance, **kwargs):

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


@receiver(post_delete, dispatch_uid=uuid.uuid4)
def deleted_object2(sender, instance, **kwargs):

    if sender in [User, Poll, Vote, Choice]:

        users_lost_badges, users_earned_badges = Badge.objects.check_badges_for_instance(instance)

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


@receiver(user_logged_in, dispatch_uid=uuid.uuid4)
def login_user(sender, request, user, **kwargs):

    notify.send(
        sender,
        user=user,
        action=Actions.USER_LOGGED_IN.value,
        target=None,
        action_target=None,
        level=Notification.SUCCESS,
    )


@receiver(user_logged_out, dispatch_uid=uuid.uuid4)
def logout_user(sender, request, user, **kwargs):

    notify.send(
        sender,
        user=user,
        action=Actions.USER_LOGGED_OUT.value,
        target=None,
        action_target=None,
        level=Notification.SUCCESS,
    )


@receiver(user_login_failed, dispatch_uid=uuid.uuid4)
def failed_login_user(sender, credentials, **kwargs):

    notify.send(
        sender,
        user=None,
        is_anonimuos=True,
        action=Actions.USER_LOGIN_FAILED.value,
        target=None,
        action_target=None,
        level=Notification.ERROR,
    )
