
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, m2m_changed, pre_save, pre_delete
from django.utils.translation import ugettext_lazy as _

from apps.accounts.models import Account
from apps.courses.models import Course
from apps.articles.models import Article
from apps.testing.models import TestingSuit
from apps.solutions.models import Solution
from apps.snippets.models import Snippet
from apps.polls.models import VoteInPoll
from apps.newsletters.models import Newsletter
from apps.questions.models import Question, Answer
from apps.forum.models import ForumTopic, ForumPost
from apps.comments.models import Comment
# from apps.replies.models import Reply
from apps.scopes.models import Scope
from apps.opinions.models import Opinion

from .models import Action


MODELS_WITH_FK_ACCOUNT = [
    Article,
    Solution,
    Snippet,
    TestingSuit,
    ForumTopic,
    ForumPost,
    Comment,
    Opinion,
    Scope,
    Newsletter,
    Question,
    Answer,
]


@receiver(pre_save)
def signal_for_keeping_old_account(sender, instance, **kwargs):
    """Write action in log."""

    if sender in MODELS_WITH_FK_ACCOUNT:
        try:
            obj = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            # it is new object
            pass
        else:
            # exists object
            if hasattr(instance, 'account'):
                instance.old_value_field_for_account = obj.account


@receiver(post_save)
def signal_created_updated_object(sender, instance, created, **kwargs):
    """Write action in log."""

    if sender in MODELS_WITH_FK_ACCOUNT:
        if hasattr(instance, 'account'):
            account = instance.account
        if created:
            Action.objects.create(
                account=account,
                flag=Action.CHOICES_FLAGS.ADD,
                message='Created {0} "{1}".'.format(instance._meta.verbose_name.lower(), instance),
            )
        else:
            Action.objects.create(
                account=account,
                flag=Action.CHOICES_FLAGS.UPDT,
                message='Updated {0} "{1}".'.format(instance._meta.verbose_name.lower(), instance),
            )
            # check on old account if here
            if account != instance.old_value_field_for_account:
                instance.old_value_field_for_account.check_badge('Dispatcher')
        # check on current account
        account.check_badge('Dispatcher')


@receiver(post_delete)
def signal_deleted_object(sender, instance, **kwargs):
    """Write action in log."""

    if sender in MODELS_WITH_FK_ACCOUNT:
        if hasattr(instance, 'account'):
            account = instance.account
        Action.objects.create(
            account=account,
            flag=Action.CHOICES_FLAGS.DEL,
            message='Deleted {0} "{1}".'.format(instance._meta.verbose_name.lower(), instance),
        )
        account.check_badge('Dispatcher')


@receiver(m2m_changed)
def signal_change_useful_links_of_solutions_or_articles(sender, instance, action, reverse, model, pk_set, **kwargs):
    """ """

    if sender in [Solution.links.through, Article.links.through]:
        if action in ['post_add', 'post_remove', 'post_clear']:
            if reverse:
                if pk_set:
                    for article_pk in pk_set:
                        account = Article.objects.get(pk=article_pk).account
                        account.check_badge('Dispatcher')
            else:
                account = instance.account
                account.check_badge('Dispatcher')


@receiver(post_delete, sender=Course)
def signal_deleted_course(sender, instance, **kwargs):

    for author in Account.objects.objects_with_badge('Sage'):
        author.check_badge('Sage')
        if not author.has_badge('Sage'):
            flag = Action.CHOICES_FLAGS.DEL
            message = 'Removed as author from the {0} "{1}".'.format(instance._meta.verbose_name.lower(), instance)
            Action.objects.create(
                account=author,
                flag=flag,
                message=message,
            )


ALL_COURSES = list()
ALL_PKS_AUTHORSHIP = list()


@receiver(m2m_changed, sender=Course.authorship.through)
def signal_change_authorhip_of_course(sender, instance, action, reverse, model, pk_set, **kwargs):
    """Write action change authorship of cource."""

    if action == 'pre_clear':
        if reverse:
            global ALL_COURSES
            ALL_COURSES = list(i.pk for i in instance.courses.all())
        else:
            global ALL_PKS_AUTHORSHIP
            ALL_PKS_AUTHORSHIP = list(i.pk for i in instance.authorship.all())

    if action in ['post_add', 'post_remove', 'post_clear']:
        if not reverse:
            if action in ['post_remove', 'post_add']:
                if action == 'post_remove':
                    flag = Action.CHOICES_FLAGS.DEL
                    message = 'Removed as author from the {0} "{1}".'.format(instance._meta.verbose_name.lower(), instance)
                elif action == 'post_add':
                    flag = Action.CHOICES_FLAGS.ADD
                    message = 'Added as author to the {0} "{1}".'.format(instance._meta.verbose_name.lower(), instance)
                for pk in pk_set:
                    account = model.objects.get(pk=pk)
                    Action.objects.create(
                        account=account,
                        flag=flag,
                        message=message,
                    )
                    account.check_badge('Sage')
            if action == 'post_clear':
                flag = Action.CHOICES_FLAGS.DEL
                message = 'Removed as author from the {0} "{1}".'.format(instance._meta.verbose_name.lower(), instance)
                for pk in ALL_PKS_AUTHORSHIP:
                    account = model.objects.get(pk=pk)
                    Action.objects.create(
                        account=account,
                        flag=flag,
                        message=message,
                    )
                    account.check_badge('Sage')
        else:
            account = instance
            if action in ['post_remove', 'post_add']:
                for pk in pk_set:
                    course = model.objects.get(pk=pk)
                    if action == 'post_remove':
                        flag = Action.CHOICES_FLAGS.DEL
                        message = 'Removed as author from the {0} "{1}".'.format(model._meta.verbose_name.lower(), course)
                    elif action == 'post_add':
                        flag = Action.CHOICES_FLAGS.ADD
                        message = 'Added as author to the {0} "{1}".'.format(model._meta.verbose_name.lower(), course)
                    Action.objects.create(
                        account=account,
                        flag=flag,
                        message=message,
                    )
            if action == 'post_clear':
                flag = Action.CHOICES_FLAGS.DEL
                for pk in ALL_COURSES:
                    course = Course.objects.get(pk=pk)
                    message = 'Removed as author from the {0} "{1}".'.format(model._meta.verbose_name.lower(), course)
                    Action.objects.create(
                        account=account,
                        flag=flag,
                        message=message,
                    )
            account.check_badge('Sage')


@receiver(post_save, sender=VoteInPoll)
def signal_account_participated_in_poll(sender, instance, **kwargs):
    """Signal, what account participated in poll."""

    Action.objects.create(
        account=instance.user,
        flag=Action.CHOICES_FLAGS.ADD,
        message='Participated in the {0} "{1}".'.format(instance.poll._meta.verbose_name.lower(), instance.poll),
    )
    instance.user.check_badge('Voter')


@receiver(post_delete, sender=VoteInPoll)
def signal_account_removed_from_voters_in_poll(sender, instance, **kwargs):
    """Signal, what account removed from voters in poll."""

    Action.objects.create(
        account=instance.user,
        flag=Action.CHOICES_FLAGS.DEL,
        message='Removed from voters in the {0} "{1}".'.format(instance.poll._meta.verbose_name.lower(), instance.poll),
    )
    instance.user.check_badge('Voter')


CHANGE_STATUS_ACCOUNT = False


@receiver(pre_save, sender=Account)
def signal_changed_status_of_account(sender, instance, **kwargs):
    """Signal attempt change status of account: is_superuser or is_active."""

    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
    else:
        global CHANGE_STATUS_ACCOUNT
        if not obj.is_superuser == instance.is_superuser:
            new_status_account = 'superuser' if instance.is_superuser else 'non superuser'
            message = 'Changed status account as {0}.'.format(new_status_account)
            Action.objects.create(
                account=instance,
                flag=Action.CHOICES_FLAGS.USER,
                message=message,
            )
            CHANGE_STATUS_ACCOUNT = True
        elif not obj.is_active == instance.is_active:
            if instance.is_active:
                message = 'Now account is active.'
            else:
                message = 'Account disabled.'
            Action.objects.create(
                account=instance,
                flag=Action.CHOICES_FLAGS.USER,
                message=message,
            )
            CHANGE_STATUS_ACCOUNT = True
        else:
            CHANGE_STATUS_ACCOUNT = False


@receiver(post_save, sender=Account)
def signal_creating_updating_of_account(sender, instance, created, **kwargs):
    """Signal creating or updating account of user."""

    global CHANGE_STATUS_ACCOUNT
    if created:
        message = 'Created account.'
    else:
        message = 'Updated account.'
    if not CHANGE_STATUS_ACCOUNT:
        Action.objects.create(
            account=instance,
            flag=Action.CHOICES_FLAGS.USER,
            message=message,
        )
    CHANGE_STATUS_ACCOUNT = False
