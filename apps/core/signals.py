
import uuid
import logging

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import pre_save, post_save, m2m_changed, pre_delete, post_delete

# from django.core.exceptions import ValidationError
# from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
# from django.conf import settings

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

from apps.notifications.signals import notify
from apps.notifications.models import Notification
from apps.notifications.constants import Action


logger = logging.getLogger('django.development')


@receiver(post_save, dispatch_uid=uuid.uuid4)
def added_update_object(sender, instance, created, **kwargs):

    if sender in [
        User, Vote, Solution, Snippet, Question, Answer, Profile, Diary,
        Article, Mark, Reply, Comment, Opinion, Post, Topic
    ]:

        if created is True:

            if sender in [Vote, Opinion, Comment, Mark, Answer, Reply, Post]:

                user = instance.user
                action_target = instance

                if sender == Vote:
                    action = Action.ADDED_VOTE
                    target = instance.poll
                elif sender == Opinion:
                    action = Action.ADDED_OPINION
                    target = instance.content_object
                elif sender == Comment:
                    action = Action.ADDED_COMMENT
                    target = instance.content_object
                elif sender == Mark:
                    action = Action.ADDED_MARK
                    target = instance.article
                elif sender == Answer:
                    action = Action.ADDED_ANSWER
                    target = instance.question
                elif sender == Reply:
                    action = Action.ADDED_REPLY
                    target = instance.book
                elif sender == Post:
                    action = Action.ADDED_POST
                    target = instance.topic

            elif sender in [Solution, Snippet, Question, Article, Topic]:
                action = Action.ADDED_OBJECT
                target = instance
                user = instance.user
                action_target = None

            elif sender == User:
                action = Action.ADDED_USER
                target = None
                action_target = None
                user = instance

        else:

            if sender in [Vote, Opinion, Comment, Mark, Answer, Reply, Post, Profile, Diary]:

                user = instance.user
                action_target = instance

                if sender == Vote:
                    target = instance.poll
                    action = Action.UPDATED_VOTE
                elif sender == Opinion:
                    target = instance.content_object
                    action = Action.UPDATED_OPINION
                elif sender == Comment:
                    target = instance.content_object
                    action = Action.UPDATED_COMMENT
                elif sender == Mark:
                    target = instance.article
                    action = Action.UPDATED_MARK
                elif sender == Answer:
                    target = instance.question
                    action = Action.UPDATED_ANSWER
                elif sender == Reply:
                    target = instance.book
                    action = Action.UPDATED_REPLY
                elif sender == Post:
                    target = instance.topic
                    action = Action.UPDATED_POST
                elif sender == Diary:
                    target = None
                    action = Action.UPDATED_DIARY
                elif sender == Profile:
                    target = None
                    action = Action.UPDATED_PROFILE

            elif sender in [Solution, Snippet, Question, Article, Topic]:
                action = Action.UPDATED_OBJECT
                action_target = None
                target = instance
                user = instance.user

            elif sender == User:
                action = Action.UPDATED_USER
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
            action = Action.DELETED_VOTE
        elif sender == Mark:
            target = instance.article
            action_target = instance
            action = Action.DELETED_MARK
        elif sender == Answer:
            target = instance.question
            action_target = instance
            action = Action.DELETED_ANSWER
        elif sender == Reply:
            target = instance.book
            action_target = instance
            action = Action.DELETED_REPLY
        elif sender == Post:
            target = instance.topic
            action_target = instance
            action = Action.DELETED_POST
        elif sender == User:
            target = None
            action_target = None
            action = Action.DELETED_USER
        elif sender == Solution:
            target = instance
            action_target = None
            action = Action.DELETED_OBJECT
        elif sender == Snippet:
            target = instance
            action_target = None
            action = Action.DELETED_OBJECT
        elif sender == Question:
            target = instance
            action_target = None
            action = Action.DELETED_OBJECT
        elif sender == Article:
            target = instance
            action_target = None
            action = Action.DELETED_OBJECT
        elif sender == Topic:
            target = instance
            action_target = None
            action = Action.DELETED_OBJECT
        elif sender == Opinion:
            target = instance.content_object
            action_target = instance
            action = Action.DELETED_OPINION
        elif sender == Comment:
            target = instance.content_object
            action_target = instance
            action = Action.DELETED_COMMENT

        notify.send(
            sender,
            user=user,
            target=target,
            action=action,
            action_target=action_target,
            level=Notification.SUCCESS,
        )


@receiver(user_logged_in, dispatch_uid=uuid.uuid4)
def login_user(sender, request, user, **kwargs):

    notify.send(
        sender,
        user=user,
        action=Action.USER_LOGGED_IN,
        target=None,
        action_target=None,
        level=Notification.SUCCESS,
    )


@receiver(user_logged_out, dispatch_uid=uuid.uuid4)
def logout_user(sender, request, user, **kwargs):

    notify.send(
        sender,
        user=user,
        action=Action.USER_LOGGED_OUT,
        target=None,
        action_target=None,
        level=Notification.SUCCESS,
    )


# @receiver(user_login_failed, dispatch_uid=uuid.uuid4)
def failed_login_user(sender, credentials, **kwargs):

    notify.send(
        sender,
        user=user,
        action=Action.USER_LOGIN_FAILED,
        target=None,
        action_target=None,
        level=Notification.SUCCESS,
    )
