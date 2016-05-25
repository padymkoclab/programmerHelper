
import collections
# import functools

from django.utils import timezone
from django.db import models

from apps.app_badges.models import GettingBadge, Badge
from apps.app_questions.models import Question, Answer
from apps.app_forum.models import ForumTopic
from apps.app_snippets.models import Snippet
from apps.app_solutions.models import Solution
from apps.app_articles.models import Article

# def point_execution_in_terminal(function):
#     """Decorator, what type point(.) in terminal when function execution."""
#     @functools.wraps(function)
#     def wrapper(self, accounts, *args, **kwargs):
#         # print('.', end='')
#         return function(self, accounts, *args, **kwargs)
#     return wrapper


class BadgeQuerySet(models.QuerySet):
    """

    """

    def last_got_badges(self, count_last_getting=10):
        """Getting listing last getting badges of accounts."""

        return GettingBadge.objects.order_by('-date_getting')[:count_last_getting]


class BadgeManager(models.Manager):
    """
    Model manager for working with badges of account
    """

    def __checkers_badges(self):
        return {
            'Favorite Question': self.check_badge_Favorite_Question,
            'Stellar Question': self.check_badge_Stellar_Question,
            'Nice Question': self.check_badge_Nice_Question,
            'Good Question': self.check_badge_Good_Question,
            'Great Question': self.check_badge_Great_Question,
            'Popular Question': self.check_badge_Popular_Question,
            'Notable Question': self.check_badge_Notable_Question,
            'Famous Question': self.check_badge_Famous_Question,
            'Schoolar': self.check_badge_Schoolar,
            'Student': self.check_badge_Student,
            'Tumbleweed': self.check_badge_Tumbleweed,
            'Enlightened': self.check_badge_Enlightened,
            'Explainer': self.check_badge_Explainer,
            'Refiner': self.check_badge_Refiner,
            'Illuminator': self.check_badge_Illuminator,
            'Guru': self.check_badge_Guru,
            'Nice Answer': self.check_badge_Nice_Answer,
            'Good Answer': self.check_badge_Good_Answer,
            'Great Answer': self.check_badge_Great_Answer,
            'Populist': self.check_badge_Populist,
            'Reversal': self.check_badge_Reversal,
            'Revival': self.check_badge_Revival,
            'Necromancer': self.check_badge_Necromancer,
            'Selflearner': self.check_badge_SelfLearner,
            'Teacher': self.check_badge_Teacher,
            'Autobiograther': self.check_badge_Autobiograther,
            'Commentator': self.check_badge_Commentator,
            'Sociable': self.check_badge_Sociable,
            'Enthusiast': self.check_badge_Enthusiast,
            'Fanatic': self.check_badge_Fanatic,
            'Eager': self.check_badge_Eager,
            'Epic': self.check_badge_Epic,
            'Legendary': self.check_badge_Legendary,
            'Citizen': self.check_badge_Citizen,
            'Talkative': self.check_badge_Talkative,
            'Outspoken': self.check_badge_Outspoken,
            'Yearning': self.check_badge_Yearning,
            'Civic Duty': self.check_badge_Civic_Duty,
            'Electorate': self.check_badge_Electorate,
            'Citizen Patrol': self.check_badge_Citizen_Patrol,
            'Depute': self.check_badge_Depute,
            'Marshal': self.check_badge_Marshal,
            'Critic': self.check_badge_Critic,
            'Nonsense': self.check_badge_Nonsense,
            'Editor': self.check_badge_Editor,
            'Organizer': self.check_badge_Organizer,
            'Proofreader': self.check_badge_Proofreader,
            'Suffrage': self.check_badge_Suffrage,
            'Vox Populi': self.check_badge_Vox_Populi,
            'Supporter': self.check_badge_Supporter,
            'Taxonomist': self.check_badge_Taxonomist,
            'Publicist': self.check_badge_Publicist,
            'Tester': self.check_badge_Tester,
            'Creator Tests': self.check_badge_Creator_Tests,
            'Clear Mind': self.check_badge_Clear_Mind,
            'Clear Head': self.check_badge_Clear_Head,
            'Closer Questions': self.check_badge_Closer_Questions,
            'Deleter Questions': self.check_badge_Deleter_Questions,
            'Dispatcher': self.check_badge_Dispatcher,
            'Sage': self.check_badge_Sage,
            'Voter': self.check_badge_Voter,
        }

    def _restrict_accounts(self, accounts, accounts_pks):
        if accounts is not None:
            if not isinstance(accounts, self.model.objects._queryset_class):
                msg = 'Parametr "accounts" must be queryset from the model "{0}"'.format(str(self.model._meta.verbose_name))
                raise TypeError(msg)
        restricted_pks = accounts.values_list('pk', flat=True)
        accounts_pks = tuple(filter(lambda x: x in restricted_pks, accounts_pks))
        return accounts_pks

    def objects_with_badge(self, badge_name):
        """Return objects with certain the badge."""

        pks = self
        for account in self.iterator():
            if not account.has_badge(badge_name):
                pks = pks.exclude(pk=account.pk)
        return pks

    def validate_badges(self, accounts=None, badges_names=None):
        # GettingBadge.objects.filter().delete()
        badges = self.__checkers_badges().items()
        if badges_names:
            if not isinstance(badges_names, (list, tuple)):
                raise TypeError('Names of badges must be as sequence.')
            all_badges_names = Badge.objects.only('name').values_list('name', flat=True)
            for badge_name in badges_names:
                if badge_name not in all_badges_names:
                    msg = 'Badge with name "{0}" does not exists.'.format(badge_name)
                    raise ValueError(msg)
            badges = {k: v for k, v in badges if k in badges_names}.items()
        for checker_name, checker_function in badges:
            # checker = point_execution_in_terminal(checker_function)
            checker_function(accounts=accounts)

    def has_badge(self, account, badge_name):
        """Checkup presence badge in account."""

        try:
            account.badges.get(badge__name__iexact=badge_name)
        except GettingBadge.DoesNotExist:
            return False
        else:
            return True

    def _added_badge_to_accounts(self, accounts_pks, badge_name):
        """Add badge to accounts listing in accounts_pks as their primary keys."""

        if accounts_pks and badge_name:
            # get badge
            badge = Badge.objects.get(badge__name__iexact=badge_name)
            # iteration on primary keys of accounts and adding badge
            for account_pk in accounts_pks:
                account = self.get(pk=account_pk)
                GettingBadge.objects.update_or_create(user=account, badge=badge)

    def check_badge_Favorite_Question(self, accounts=None):
        """Question if favorited at least 5 users."""

        all_questions_with_certain_favorites = Question.objects.questions_by_min_count_favorits(min_count_favorits=5)
        accounts_pks = all_questions_with_certain_favorites.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='favorite question')

    def check_badge_Stellar_Question(self, accounts=None):
        """Question if favorited at least 10 users."""

        all_questions_with_certain_favorites = Question.objects.questions_by_min_count_favorits(
            min_count_favorits=10,
        )
        accounts_pks = all_questions_with_certain_favorites.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='stellar question')

    def check_badge_Nice_Question(self, accounts=None):
        """Scope of question must be 5 and more."""

        nices_questions = Question.objects.questions_by_scopes(min_scope=5)
        accounts_pks = nices_questions.values_list('author', flat=True)
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='nice question')

    def check_badge_Good_Question(self, accounts=None):
        """Scope of question must be 10 and more."""

        SCOPE_QUESTION_AS_GOOD = 10
        nices_questions = Question.objects.questions_by_scopes(min_scope=SCOPE_QUESTION_AS_GOOD)
        accounts_pks = nices_questions.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='good question')

    def check_badge_Great_Question(self, accounts=None):
        """Scope of question must be 20 and more."""

        SCOPE_QUESTION_AS_GREAT = 20
        nices_questions = Question.objects.questions_by_scopes(min_scope=SCOPE_QUESTION_AS_GREAT)
        accounts_pks = nices_questions.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='great question')

    def check_badge_Popular_Question(self, accounts=None):
        """Count views of question must be 100 and more."""

        COUNT_VIEWS_QUESTION_AS_POPULAR = 100
        questions = Question.objects.filter(views__gte=COUNT_VIEWS_QUESTION_AS_POPULAR)
        accounts_pks = questions.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='popular question')

    def check_badge_Notable_Question(self, accounts=None):
        """Count views of question must be 500 and more."""

        COUNT_VIEWS_QUESTION_AS_NOTABLE = 500
        questions = Question.objects.filter(views__gte=COUNT_VIEWS_QUESTION_AS_NOTABLE)
        accounts_pks = questions.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='notable question')

    def check_badge_Famous_Question(self, accounts=None):
        """Count views of question must be 1000 and more."""

        questions = Question.objects.filter(views__gte=1000)
        accounts_pks = questions.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='famous question')

    def check_badge_Schoolar(self, accounts=None):
        """Have question with acceptabled answer."""

        accounts_pks = Answer.objects.accepted_answers().values_list('question__author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='schoolar')

    def check_badge_Student(self, accounts=None):
        """Accept an answers on 5 questions."""

        undistinct_account_pks = Answer.objects.accepted_answers().values_list('question__author', flat=True)
        counter_undistinct_account_pks = collections.Counter(undistinct_account_pks)
        # choice accounts satisfied restriction
        tuple_with_account_pks_and_count_accepted_answers = filter(
            lambda item: item[1] >= 5,
            counter_undistinct_account_pks.items(),
        )
        # replace two-nested tuple on single-nested tuple with removing count accepted answer,
        # left only primary keyes of accounts
        accounts_pks = tuple(item[0] for item in tuple_with_account_pks_and_count_accepted_answers)
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='student')

    def check_badge_Tumbleweed(self, accounts=None):
        """Asked a question with zero score or less, no answers."""

        non_interesting_questions = Question.objects.non_interesting_questions()
        accounts_pks = non_interesting_questions.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='tumbleweed')

    def check_badge_Enlightened(self, accounts=None):
        """Had accepted answer with score of 10 or more."""

        MIN_SCOPE_ANSWER_FOR_ENLIGHTENED = 10
        answers_with_min_scope = Answer.objects.answers_by_scopes(min_scope=MIN_SCOPE_ANSWER_FOR_ENLIGHTENED)
        accepted_answers = Answer.objects.accepted_answers()
        accepted_answers_with_min_scope = answers_with_min_scope & accepted_answers
        accounts_pks = accepted_answers_with_min_scope.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='enlightened')

    def check_badge_Explainer(self, accounts=None):
        """Answer on 1 question within 24 hours and with scope > 0."""

        useful_answers = Answer.objects.answers_by_scopes(min_scope=1)
        quickly_answers = Answer.objects.quickly_answers()
        useful_quickly_answers = useful_answers & quickly_answers
        accounts_pks = useful_quickly_answers.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='explainer')

    def check_badge_Refiner(self, accounts=None):
        """Answer on 5 questions within 24 hours and with scope > 0."""

        useful_answers = Answer.objects.answers_by_scopes(min_scope=1)
        quickly_answers = Answer.objects.quickly_answers()
        useful_quickly_answers = useful_answers & quickly_answers
        undistinct_account_pks = useful_quickly_answers.values_list('author', flat=True)
        counter_undistinct_account_pks = collections.Counter(undistinct_account_pks)
        # choice accounts satisfied restriction
        tuple_with_account_pks_and_count_answers = filter(
            lambda item: item[1] >= 5,
            counter_undistinct_account_pks.items(),
        )
        # replace two-nested tuple on single-nested tuple with removing count accepted answer,
        # left only primary keyes of accounts
        accounts_pks = tuple(item[0] for item in tuple_with_account_pks_and_count_answers)
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='refiner')

    def check_badge_Illuminator(self, accounts=None):
        """Answer on 10 questions within 24 hours and with scope > 0."""

        useful_answers = Answer.objects.answers_by_scopes(min_scope=1)
        quickly_answers = Answer.objects.quickly_answers()
        useful_quickly_answers = useful_answers & quickly_answers
        undistinct_account_pks = useful_quickly_answers.values_list('author', flat=True)
        counter_undistinct_account_pks = collections.Counter(undistinct_account_pks)
        # choice accounts satisfied restriction
        tuple_with_account_pks_and_count_answers = filter(
            lambda item: item[1] >= 10,
            counter_undistinct_account_pks.items(),
        )
        # replace two-nested tuple on single-nested tuple with removing count accepted answer,
        # left only primary keyes of accounts
        accounts_pks = tuple(item[0] for item in tuple_with_account_pks_and_count_answers)
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='illuminator')

    def check_badge_Guru(self, accounts=None):
        """Given accepted answer with score of 5 or more."""

        useful_answers = Answer.objects.answers_by_scopes(min_scope=5)
        accepted_answers = Answer.objects.accepted_answers()
        good_accepted_answers = useful_answers & accepted_answers
        accounts_pks = good_accepted_answers.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='guru')

    def check_badge_Nice_Answer(self, accounts=None):
        """Answer score of 5 or more."""

        answers = Answer.objects.answers_by_scopes(min_scope=5)
        accounts_pks = answers.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='nice answer')

    def check_badge_Good_Answer(self, accounts=None):
        """Answer score of 10 or more."""

        answers = Answer.objects.answers_by_scopes(min_scope=10)
        accounts_pks = answers.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='good answer')

    def check_badge_Great_Answer(self, accounts=None):
        """Answer score of 15 or more."""

        answers = Answer.objects.answers_by_scopes(min_scope=15)
        accounts_pks = answers.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='great answer')

    def check_badge_Populist(self, accounts=None):
        """Highest scoring answer that outscored an accepted answer."""
        #
        #
        #

    def check_badge_Reversal(self, accounts=None):
        """Provide an answer of +1 and more score to a question of -1 and less score."""

        questions_by_max_scope = Question.objects.questions_by_scopes(max_scope=-1)
        answers_by_min_scope = Answer.objects.answers_by_scopes(min_scope=1)
        pks_answers_with_questions_by_max_scope = questions_by_max_scope.values_list('answers', flat=True).distinct()
        reversal_answers = answers_by_min_scope.filter(pk__in=pks_answers_with_questions_by_max_scope)
        accounts_pks = reversal_answers.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='reversal')

    def check_badge_Revival(self, accounts=None):
        """Answer more than 7 days after a question was asked."""

        revival_answers = Answer.objects.revival_answers(count_days=7)
        accounts_pks = revival_answers.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='revival')

    def check_badge_Necromancer(self, accounts=None):
        """Answer a question more than 7 days later with score of 5 or more."""

        revival_answers = Answer.objects.revival_answers(count_days=7)
        answers_by_min_scope = Answer.objects.answers_by_scopes(min_scope=5)
        revival_answers_by_min_scope = answers_by_min_scope & revival_answers
        accounts_pks = revival_answers_by_min_scope.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='necromancer')

    def check_badge_SelfLearner(self, accounts=None):
        """Answer your own question with score of 1 or more."""

        answers = Answer.objects.answers_with_scopes().filter(question__author=models.F('author')).filter(scope__gte=1)
        accounts_pks = answers.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='self-learner')

    def check_badge_Teacher(self, accounts=None):
        """Answer a question with score of 1 or more."""

        answers = Answer.objects.answers_with_scopes().filter(scope__gte=1)
        accounts_pks = answers.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='teacher')

    def check_badge_Autobiograther(self, accounts=None):
        """Completed fill up account profile."""

        accounts_pks = list()
        filled_accounts_profiles = self.model.objects.get_filled_accounts_profiles()
        for account_pk, percent in filled_accounts_profiles.items():
            if percent == 100:
                accounts_pks.append(account_pk)
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='autobiograther')

    def check_badge_Commentator(self, accounts=None):
        """Leave 10 comments."""

        accounts_with_count_comments = self.model.objects.annotate(count_comments=models.Count('comments', distinct=True))
        commentators = accounts_with_count_comments.filter(count_comments__gte=10)
        accounts_pks = commentators.values_list('pk', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='commentator')

    def check_badge_Sociable(self, accounts=None):
        """Leave 20 comments."""

        accounts_with_count_comments = self.model.objects.annotate(count_comments=models.Count('comments', distinct=True))
        commentators = accounts_with_count_comments.filter(count_comments__gte=20)
        accounts_pks = commentators.values_list('pk', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='sociable')

    def check_badge_Enthusiast(self, accounts=None):
        """Visit the site each day for 5 consecutive days."""

        accounts_pks = list()
        for account in self.model.objects.iterator():
            if account.have_certain_count_consecutive_days(5):
                accounts_pks.append(account.pk)
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='Enthusiast')

    def check_badge_Fanatic(self, accounts=None):
        """Visit the site each day for 10 consecutive days."""

        accounts_pks = list()
        for account in self.model.objects.iterator():
            if account.have_certain_count_consecutive_days(10):
                accounts_pks.append(account.pk)
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='Fanatic')

    def check_badge_Eager(self, accounts=None):
        """Earn reputation 100 and more."""
        accounts_pks = list()
        for account in self.iterator():
            if account.get_reputation() >= 100:
                accounts_pks.append(account.pk)
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='eager')

    def check_badge_Epic(self, accounts=None):
        """Earn reputation 1000 and more."""

        accounts_pks = list()
        for account in self.iterator():
            if account.get_reputation() >= 1000:
                accounts_pks.append(account.pk)
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='epic')

    def check_badge_Legendary(self, accounts=None):
        """Earn reputation 10000 and more."""

        accounts_pks = list()
        for account in self.iterator():
            if account.get_reputation() >= 10000:
                accounts_pks.append(account.pk)
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='legendary')

    def check_badge_Citizen(self, accounts=None):
        """Have more than 1 post on forum."""

        accounts_with_one_or_more_posts = ForumTopic.objects.topics_with_count_posts().filter(count_posts__gte=1)
        accounts_pks = accounts_with_one_or_more_posts.values_list('author', flat=True)
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='citizen')

    def check_badge_Talkative(self, accounts=None):
        """Have more than 10 post on forum."""

        accounts_with_one_or_more_posts = ForumTopic.objects.topics_with_count_posts().filter(count_posts__gte=10)
        accounts_pks = accounts_with_one_or_more_posts.values_list('author', flat=True)
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='citizen')

    def check_badge_Outspoken(self, accounts=None):
        """Have more than 15 post on forum."""

        accounts_with_one_or_more_posts = ForumTopic.objects.topics_with_count_posts().filter(count_posts__gte=15)
        accounts_pks = accounts_with_one_or_more_posts.values_list('author', flat=True)
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='citizen')

    def check_badge_Yearning(self, accounts=None):
        """Active member for a year, earning at least 200 reputation."""

        accounts_pks = list()
        for account in self.iterator():
            if account.get_reputation() >= 200 and account.date_joined <= timezone.now() - timezone.timedelta(days=365):
                accounts_pks.append(account.pk)
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='yearning')

    def check_badge_Civic_Duty(self, accounts=None):
        """Given 10 opinions or more times."""

        civic_duty = self.model.objects.objects_with_count_opinions().filter(count_opinions__gte=10)
        accounts_pks = civic_duty.values_list('pk', flat=True)
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='civic duty')

    def check_badge_Electorate(self, accounts=None):
        """Given 15 opinions or more times."""

        electorate = self.model.objects.objects_with_count_opinions().filter(count_opinions__gte=15)
        accounts_pks = electorate.values_list('pk', flat=True)
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='electorate')

    def check_badge_Citizen_Patrol(self, accounts=None):
        """Have 5 and more favorited objects."""

        accounts_with_count_favorites_and_unfavorites = self.model.objects.objects_with_count_favorites_and_unfavorites()
        accounts_as_citizen_patrol = accounts_with_count_favorites_and_unfavorites.filter(count_favorites__gte=5)
        accounts_pks = accounts_as_citizen_patrol.values_list('pk', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='citizen patrol')

    def check_badge_Depute(self, accounts=None):
        """Have 10 and more favorited objects."""

        accounts_with_count_favorites_and_unfavorites = self.model.objects.objects_with_count_favorites_and_unfavorites()
        accounts_as_citizen_patrol = accounts_with_count_favorites_and_unfavorites.filter(count_favorites__gte=10)
        accounts_pks = accounts_as_citizen_patrol.values_list('pk', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='depute')

    def check_badge_Marshal(self, accounts=None):
        """Have 15 and more favorited objects."""

        accounts_with_count_favorites_and_unfavorites = self.model.objects.objects_with_count_favorites_and_unfavorites()
        accounts_as_citizen_patrol = accounts_with_count_favorites_and_unfavorites.filter(count_favorites__gte=15)
        accounts_pks = accounts_as_citizen_patrol.values_list('pk', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='marshal')

    def check_badge_Critic(self, accounts=None):
        """Have answer with scope -3 and less."""

        critic_answers = Answer.objects.answers_by_scopes(max_scope=-3)
        accounts_pks = critic_answers.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='critic')

    def check_badge_Nonsense(self, accounts=None):
        """Have question with scope -3 and less."""

        nonsense_questions = Question.objects.questions_by_scopes(max_scope=-3)
        accounts_pks = nonsense_questions.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='nonsense')

    def check_badge_Editor(self, accounts=None):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # if accounts is not None:
        #     accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        # self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='editor')

    def check_badge_Organizer(self, accounts=None):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # if accounts is not None:
        #     accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        # self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='organizer')

    def check_badge_Proofreader(self, accounts=None):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # if accounts is not None:
        #     accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        # self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='proofreader')

    def check_badge_Suffrage(self, accounts=None):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # if accounts is not None:
        #     accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        # self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='suffrage')

    def check_badge_Vox_Populi(self, accounts=None):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # if accounts is not None:
        #     accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        # self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='vox_populi')

    def check_badge_Supporter(self, accounts=None):
        """Have answer and question with scope +3 and more."""

        good_answers = Answer.objects.answers_by_scopes(min_scope=3)
        good_questions = Question.objects.questions_by_scopes(min_scope=3)
        authors_good_answers = good_answers.values_list('author', flat=True)
        authors_good_questions = good_questions.values_list('author', flat=True)
        authors_good_answers_and_questions = frozenset(authors_good_answers) & frozenset(authors_good_questions)
        if accounts is not None:
            authors_good_answers_and_questions = self._restrict_accounts(accounts, authors_good_answers_and_questions)
        self._added_badge_to_accounts(accounts_pks=authors_good_answers_and_questions, badge_name='supporter')

    def check_badge_Taxonomist(self, accounts=None):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_a

    def check_badge_Publicist(self, accounts=None):
        """Publicated own article."""

        publicists = self.model.objects.objects_with_count_articles().filter(count_articles__gte=1)
        accounts_pks = publicists.values_list('pk', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='publicist')

    def check_badge_Tester(self, accounts=None):
        """Passed at leat 1 testsuit."""

        accaunts_passages_testsuits = self.model.objects.objects_passages_testsuits()
        accounts_pks = accaunts_passages_testsuits.values_list('pk', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='tester')

    def check_badge_Creator_Tests(self, accounts=None):
        """Create own testing suit."""

        creators_testing_suits = self.model.objects.creators_testing_suits()
        accounts_pks = creators_testing_suits.values_list('pk', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='creator tests')

    def check_badge_Clear_Mind(self, accounts=None):
        """Added own solution with scope +1 or more."""

        solutions_by_min_scope = Solution.objects.solutions_by_scopes(min_scope=1)
        accounts_pks = solutions_by_min_scope.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='clear mind')

    def check_badge_Clear_Head(self, accounts=None):
        """Added own snippet with scope +1 or more."""

        badge_name = 'Clear Head'
        badge = Badge.objects.get(name__iexact=badge_name)

        if accounts is None:
            accounts = self.iterator()
        # for account in accounts:
        #     if not account.has_badge(badge_name):
        #         if account.articles.filter(links__isnull=False).count() or \
        #                 account.solutions.filter(links__isnull=False).count():
        #             GettingBadge.objects.create(user=account, badge=badge)
        #     if account.has_badge(badge_name):
        #         if not account.articles.filter(links__isnull=False).count() and \
        #                 not account.solutions.filter(links__isnull=False).count():
        #             GettingBadge.objects.get(user=account, badge=badge).delete()
        snippets_by_min_scope = Snippet.objects.snippets_by_scopes(min_scope=1)
        accounts_pks = snippets_by_min_scope.values_list('author', flat=True).distinct()
        if accounts is not None:
            accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='clear head')

    def check_badge_Closer_Questions(self, accounts=None):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # if accounts is not None:
        #     accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        # self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='closer_questions')

    def check_badge_Deleter_Questions(self, accounts=None):
        """ """

        # accounts_pks = answers.values_list('author', flat=True).distinct()
        # if accounts is not None:
        #     accounts_pks = self._restrict_accounts(accounts, accounts_pks)
        # self._added_badge_to_accounts(accounts_pks=accounts_pks, badge_name='deleter_questions')

    def check_badge_Dispatcher(self, accounts=None):
        """Used links in own articles or solutions."""

        badge_name = 'Dispatcher'
        badge = Badge.objects.get(name__iexact=badge_name)

        if accounts is None:
            accounts = self.iterator()
        for account in accounts:
            if not account.has_badge(badge_name):
                if account.articles.filter(links__isnull=False).count() or \
                        account.solutions.filter(links__isnull=False).count():
                    GettingBadge.objects.create(user=account, badge=badge)
            if account.has_badge(badge_name):
                if not account.articles.filter(links__isnull=False).count() and \
                        not account.solutions.filter(links__isnull=False).count():
                    GettingBadge.objects.get(user=account, badge=badge).delete()

    def check_badge_Sage(self, accounts=None):
        """Participated in creating courses."""

        badge_name = 'Sage'
        badge = Badge.objects.get(name__iexact=badge_name)

        if accounts is None:
            accounts = self.iterator()
        for account in accounts:
            if not account.has_badge(badge_name) and account.courses.count():
                GettingBadge.objects.create(user=account, badge=badge)
            if account.has_badge(badge_name) and not account.courses.count():
                GettingBadge.objects.get(user=account, badge=badge).delete()

    def check_badge_Voter(self, accounts=None):
        """Voted in polls."""

        badge_name = 'Voter'
        badge = Badge.objects.get(name__iexact=badge_name)

        if accounts is None:
            accounts = self.iterator()
        for account in accounts:
            if not account.has_badge(badge_name) and account.votes_in_polls.count():
                GettingBadge.objects.create(user=account, badge=badge)
            if account.has_badge(badge_name) and not account.votes_in_polls.count():
                GettingBadge.objects.get(user=account, badge=badge).delete()
