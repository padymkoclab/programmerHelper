
import uuid

from django.db.models.signals import pre_save, post_save, m2m_changed, pre_delete, post_delete

# from django.core.exceptions import ValidationError
# from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
# from django.conf import settings

from apps.users.models import User
from apps.polls.models import Vote
from apps.snippets.models import Snippet
from apps.solutions.models import Solution
from apps.articles.models import Article, Mark
from apps.questions.models import Question, Answer
from apps.forums.models import Topic, Post

from apps.library.models import Reply
from apps.comments.models import Comment
from apps.opinions.models import Opinion

from apps.notifications.signals import notify


@receiver(post_save, dispatch_uid=uuid.uuid4)
def added_update_object(sender, instance, created, **kwargs):

    if sender in [User, Vote, Solution, Snippet, Question, Answer, Article, Mark, Reply, Comment, Opinion, Post, Topic]:

        if created is True:

            if sender in [Vote, Opinion, Comment, Mark, Answer, Reply]:

                actor = instance.user

                if sender == Vote:
                    action = 'added vote to'
                    target = instance.poll
                elif sender == Opinion:
                    action = 'added opinion to'
                    target = instance.content_object
                elif sender == Comment:
                    action = 'added comment to'
                    target = instance.content_object
                elif sender == Mark:
                    action = 'added mark to'
                    target = instance.article
                elif sender == Answer:
                    action = 'added answer to'
                    target = instance.question
                elif sender == Reply:
                    action = 'added reply to'
                    target = instance.book

            elif sender in [Solution, Snippet, Question, Article, Post, Topic]:
                action = 'created'
                target = instance
                actor = instance.user

            elif sender == User:
                action = 'registered'
                target = None
                actor = instance

        else:

            if sender in [Vote, Opinion, Comment, Mark, Answer, Reply]:

                actor = instance.user

                if sender == Vote:
                    target = instance.poll
                    action = 'update vote to'
                elif sender == Opinion:
                    target = instance.content_object
                    action = 'update opinion to'
                elif sender == Comment:
                    target = instance.content_object
                    action = 'update comment to'
                elif sender == Mark:
                    target = instance.article
                    action = 'update mark to'
                elif sender == Answer:
                    target = instance.question
                    action = 'update answer to'
                elif sender == Reply:
                    target = instance.book
                    action = 'update reply to'

            elif sender in [Solution, Snippet, Question, Article, Post, Topic]:
                action = 'updated'
                target = instance
                actor = instance.user

            elif sender == User:
                action = 'updated'
                target = None
                actor = instance

        notify.send(sender, actor=actor, target=target, action=action)


@receiver(post_delete, dispatch_uid=uuid.uuid4)
def deleted_object(sender, instance, **kwargs):

    if sender in [User, Vote, Solution, Snippet, Question, Answer, Article, Mark, Reply, Comment, Opinion, Post, Topic]:

        if sender in [Vote, Opinion, Comment, Mark, Answer, Reply]:

            actor = instance.user

            if sender == Vote:
                target = instance.poll
                action = 'deteted vote on'
            elif sender == Opinion:
                target = instance.content_object
                action = 'deleted opinion on'
            elif sender == Comment:
                target = instance.content_object
                action = 'deleted comment on'
            elif sender == Mark:
                target = instance.article
                action = 'deleted mark on'
            elif sender == Answer:
                target = instance.question
                action = 'deleted answer on'
            elif sender == Reply:
                target = instance.book
                action = 'deleted reply on'

        elif sender in [Solution, Snippet, Question, Article, Post, Topic]:
            action = 'deleted'
            target = instance
            actor = instance.user

        elif sender == User:
            action = 'deleted'
            target = None
            actor = instance

        notify.send(sender, actor=actor, target=target, action=action)
