
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, m2m_changed, pre_save, pre_delete

from apps.app_accounts.models import Account
from apps.app_courses.models import Course
from apps.app_articles.models import Article
from apps.app_testing.models import TestingSuit
from apps.app_solutions.models import Solution
from apps.app_snippets.models import Snippet
from apps.app_polls.models import VoteInPoll
from apps.app_newsletters.models import Newsletter
from apps.app_questions.models import Question, Answer
from apps.app_forum.models import ForumTopic, ForumPost
from apps.app_generic_models.models import CommentGeneric, OpinionGeneric, LikeGeneric, ScopeGeneric

from .models import Action


MODELS_WITH_FK_ACCOUNT = [
    Article,
    Solution,
    Snippet,
    TestingSuit,
    ForumTopic,
    ForumPost,
    CommentGeneric,
    OpinionGeneric,
    LikeGeneric,
    ScopeGeneric,
    Newsletter,
    Question,
    Answer,
]


OLD_ACCOUNT = None

@receiver(pre_save)
def signal_for_keeping_old_account(sender, instance, **kwargs):
    """Write action in log."""

    if sender in MODELS_WITH_FK_ACCOUNT:
        try:
            obj = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            pass
        else:
            if hasattr(instance, 'author'):
                account = instance.author
                old_account = obj.author
            elif hasattr(instance, 'user'):
                account = instance.user
                old_account = obj.user
            global OLD_ACCOUNT
            if account != old_account:
                OLD_ACCOUNT = old_account
            else:
                OLD_ACCOUNT = None


@receiver(post_save)
def signal_created_updated_object(sender, instance, created, **kwargs):
    """Write action in log."""

    if sender in MODELS_WITH_FK_ACCOUNT:
        if hasattr(instance, 'author'):
            account = instance.author
        elif hasattr(instance, 'user'):
            account = instance.user
        if created:
            Action.objects.create(
                account=account,
                flag=Action.CHOICES_FLAGS.adding,
                message='Created new {0} "{1}".'.format(instance._meta.verbose_name.lower(), instance),
            )
        else:
            Action.objects.create(
                account=account,
                flag=Action.CHOICES_FLAGS.updating,
                message='Updated {0} "{1}".'.format(instance._meta.verbose_name.lower(), instance),
            )
        # check on current account
        account.check_badge('Dispatcher')
        # check on old account if here
        if OLD_ACCOUNT is not None:
            OLD_ACCOUNT.check_badge('Dispatcher')


@receiver(post_delete)
def signal_deleted_object(sender, instance, **kwargs):
    """Write action in log."""

    if sender in MODELS_WITH_FK_ACCOUNT:
        # import ipdb; ipdb.set_trace()
        if hasattr(instance, 'author'):
            account = instance.author
        elif hasattr(instance, 'user'):
            account = instance.user
        Action.objects.create(
            account=account,
            flag=Action.CHOICES_FLAGS.deleting,
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
                        account = Article.objects.get(pk=article_pk).author
                        account.check_badge('Dispatcher')
            else:
                account = instance.author
                account.check_badge('Dispatcher')


@receiver(post_delete, sender=Course)
def signal_deleted_course(sender, instance, **kwargs):

    for author in Account.objects.objects_with_badge('Sage'):
        author.check_badge('Sage')


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
                    flag = Action.CHOICES_FLAGS.deleting
                    message = 'Removed as author from {0} "{1}".'.format(instance._meta.verbose_name.lower(), instance)
                elif action == 'post_add':
                    flag = Action.CHOICES_FLAGS.adding
                    message = 'Added as author to {0} "{1}".'.format(instance._meta.verbose_name.lower(), instance)
                for pk in pk_set:
                    account = model.objects.get(pk=pk)
                    Action.objects.create(
                        account=account,
                        flag=flag,
                        message=message,
                    )
                    account.check_badge('Sage')
            if action == 'post_clear':
                flag = Action.CHOICES_FLAGS.deleting
                message = 'Removed as author from {0} "{1}".'.format(instance._meta.verbose_name.lower(), instance)
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
                        flag = Action.CHOICES_FLAGS.deleting
                        message = 'Removed as author from {0} "{1}".'.format(model._meta.verbose_name.lower(), course)
                    elif action == 'post_add':
                        flag = Action.CHOICES_FLAGS.adding
                        message = 'Added as author to {0} "{1}".'.format(model._meta.verbose_name.lower(), course)
                    Action.objects.create(
                        account=account,
                        flag=flag,
                        message=message,
                    )
            if action == 'post_clear':
                flag = Action.CHOICES_FLAGS.deleting
                for pk in ALL_COURSES:
                    course = Course.objects.get(pk=pk)
                    message = 'Removed as author from {0} "{1}".'.format(model._meta.verbose_name.lower(), course)
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
        flag=Action.CHOICES_FLAGS.adding,
        message='Participated in {0} "{1}".'.format(instance.poll._meta.verbose_name.lower(), instance.poll),
    )
    instance.user.check_badge('Voter')


@receiver(post_delete, sender=VoteInPoll)
def signal_account_removed_from_voters_in_poll(sender, instance, **kwargs):
    """Signal, what account removed from voters in poll."""
    Action.objects.create(
        account=instance.user,
        flag=Action.CHOICES_FLAGS.deleting,
        message='Removed from voters in {0} "{1}".'.format(instance.poll._meta.verbose_name.lower(), instance.poll),
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
            message = 'Change status account as {0}.'.format(new_status_account)
            Action.objects.create(
                account=instance,
                flag=Action.CHOICES_FLAGS.profiling,
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
                flag=Action.CHOICES_FLAGS.profiling,
                message=message,
            )
            CHANGE_STATUS_ACCOUNT = True
        else:
            CHANGE_STATUS_ACCOUNT = False


@receiver(post_save, sender=Account)
def signal_creating_updating_of_account(sender, instance, created, **kwargs):
    """Signal creating or update account of user."""
    global CHANGE_STATUS_ACCOUNT
    if created:
        message = 'Created account'
    else:
        message = 'Update account'
    if not CHANGE_STATUS_ACCOUNT:
        Action.objects.create(
            account=instance,
            flag=Action.CHOICES_FLAGS.profiling,
            message=message,
        )
    CHANGE_STATUS_ACCOUNT = False


@receiver(post_delete, sender=Account)
def signal_deleted_account(sender, instance, **kwargs):
    """Signal creating or update account of user."""
    message = 'Delete {0} "{1.username} ({1.email})"'.format(instance._meta.verbose_name.lower(), instance)
    Action.objects.create(
        account=instance,
        flag=Action.CHOICES_FLAGS.profiling,
        message=message,
    )
