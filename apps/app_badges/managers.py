
import collections
import functools

from django.db import models

from apps.app_badges.models import GettingBadge, Badge
from apps.app_questions.models import Question, Answer


def point_execution_in_terminal(function):
    """Decorator, what type point(.) in terminal when function execution."""
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        print('.')
        return function(*args, **kwargs)
    return wrapper


class BadgeManager(models.Manager):
    """
    Model manager for working with badges of account
    """
    def validate_badges(self, account_natural_key=None):
        # account = get_user_model().objects.get_by_natural_key(account_natural_key)
        GettingBadge.objects.filter().delete()
        # print('[', end='')
        self.check_badge_Favorite_Question()
        self.check_badge_Stellar_Question()
        self.check_badge_Nice_Question()
        self.check_badge_Good_Question()
        self.check_badge_Great_Question()
        self.check_badge_Popular_Question()
        self.check_badge_Notable_Question()
        self.check_badge_Famous_Question()
        self.check_badge_Schoolar()
        self.check_badge_Student()
        self.check_badge_Tumbleweed()
        self.check_badge_Enlightened()
        self.check_badge_Explainer()
        self.check_badge_Refiner()
        self.check_badge_Illuminator()
        self.check_badge_Guru()
        # print(']', end='')

    def has_badge(self, account, badge):
        """Checkup presence badge in account."""
        try:
            GettingBadge.objects.get(account=account, badge=badge)
        except GettingBadge.DoesNotExist:
            return False
        else:
            return True

    def get_badges(self, account):
        """Getting all badges certain account."""
        pass

    def last_got_badges(self, count_last_getting=10):
        """Getting listing last getting badges of accounts."""
        return GettingBadge.objects.order_by('-date_getting')[:count_last_getting]

    def added_badge_to_accounts(self, account_pks, badge_name):
        """Add badge to accounts listing in account_pks as their primary keys."""
        if account_pks and badge_name:
            # get badge
            badge = Badge.objects.get(name__icontains=badge_name)
            # iteration on primary keys of accounts and adding badge
            for account_pk in account_pks:
                account = self.get(pk=account_pk)
                GettingBadge.objects.update_or_create(user=account, badge=badge)

    @point_execution_in_terminal
    def check_badge_Favorite_Question(self):
        """Question if favorited at least 5 users."""
        QUESTION_AS_FAVORITE = 5
        all_questions_with_certain_favorites = Question.objects.questions_by_min_count_favorits(
            min_count_favorits=QUESTION_AS_FAVORITE,
        )
        account_pks = all_questions_with_certain_favorites.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='favorite question')

    @point_execution_in_terminal
    def check_badge_Stellar_Question(self):
        """Question if favorited at least 10 users."""
        QUESTION_AS_STELLAR = 10
        all_questions_with_certain_favorites = Question.objects.questions_by_min_count_favorits(
            min_count_favorits=QUESTION_AS_STELLAR,
        )
        account_pks = all_questions_with_certain_favorites.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='stellar question')

    @point_execution_in_terminal
    def check_badge_Nice_Question(self):
        """Scope of question must be 5 and more."""
        SCOPE_QUESTION_AS_NICE = 5
        nices_questions = Question.objects.questions_by_min_scope(min_scope=SCOPE_QUESTION_AS_NICE)
        account_pks = nices_questions.values_list('author', flat=True)
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='nice question')

    @point_execution_in_terminal
    def check_badge_Good_Question(self):
        """Scope of question must be 10 and more."""
        SCOPE_QUESTION_AS_GOOD = 10
        nices_questions = Question.objects.questions_by_min_scope(min_scope=SCOPE_QUESTION_AS_GOOD)
        account_pks = nices_questions.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='good question')

    @point_execution_in_terminal
    def check_badge_Great_Question(self):
        """Scope of question must be 20 and more."""
        SCOPE_QUESTION_AS_GREAT = 20
        nices_questions = Question.objects.questions_by_min_scope(min_scope=SCOPE_QUESTION_AS_GREAT)
        account_pks = nices_questions.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='great question')

    @point_execution_in_terminal
    def check_badge_Popular_Question(self):
        """Count views of question must be 100 and more."""
        COUNT_VIEWS_QUESTION_AS_POPULAR = 100
        questions = Question.objects.filter(views__gte=COUNT_VIEWS_QUESTION_AS_POPULAR)
        account_pks = questions.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='popular question')

    @point_execution_in_terminal
    def check_badge_Notable_Question(self):
        """Count views of question must be 500 and more."""
        COUNT_VIEWS_QUESTION_AS_NOTABLE = 500
        questions = Question.objects.filter(views__gte=COUNT_VIEWS_QUESTION_AS_NOTABLE)
        account_pks = questions.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='notable question')

    @point_execution_in_terminal
    def check_badge_Famous_Question(self):
        """Count views of question must be 1000 and more."""
        COUNT_VIEWS_QUESTION_AS_FAMOUS = 1000
        questions = Question.objects.filter(views__gte=COUNT_VIEWS_QUESTION_AS_FAMOUS)
        account_pks = questions.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='famous question')

    @point_execution_in_terminal
    def check_badge_Schoolar(self):
        """Have question with acceptabled answer."""
        account_pks = Answer.objects.accepted_answers().values_list('question__author', flat=True).distinct()
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='schoolar')

    @point_execution_in_terminal
    def check_badge_Student(self):
        """Accept an answers on 5 questions."""
        NECESSARY_COUNT_ACCEPTED_ANSWERS = 5
        undistinct_account_pks = Answer.objects.accepted_answers().values_list('question__author', flat=True)
        counter_undistinct_account_pks = collections.Counter(undistinct_account_pks)
        # choice accounts satisfied restriction
        tuple_with_account_pks_and_count_accepted_answers = filter(
            lambda item: item[1] >= NECESSARY_COUNT_ACCEPTED_ANSWERS,
            counter_undistinct_account_pks.items(),
        )
        # replace two-nested tuple on single-nested tuple with removing count accepted answer,
        # left only primary keyes of accounts
        account_pks = tuple(item[0] for item in tuple_with_account_pks_and_count_accepted_answers)
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='student')

    @point_execution_in_terminal
    def check_badge_Tumbleweed(self):
        """Asked a question with zero score or less, no answers."""
        non_interesting_questions = Question.objects.non_interesting_questions()
        account_pks = non_interesting_questions.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='tumbleweed')

    @point_execution_in_terminal
    def check_badge_Enlightened(self):
        """Had accepted answer with score of 10 or more."""
        MIN_SCOPE_ANSWER_FOR_ENLIGHTENED = 10
        answers_with_min_scope = Answer.objects.answers_by_min_scope(min_scope=MIN_SCOPE_ANSWER_FOR_ENLIGHTENED)
        accepted_answers = Answer.objects.accepted_answers()
        accepted_answers_with_min_scope = answers_with_min_scope & accepted_answers
        account_pks = accepted_answers_with_min_scope.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='enlightened')

    @point_execution_in_terminal
    def check_badge_Explainer(self):
        """Answer on 1 question within 24 hours and with scope > 0."""
        useful_answers = Answer.objects.answers_by_min_scope(min_scope=1)
        quickly_answers = Answer.objects.quickly_answers()
        useful_quickly_answers = useful_answers & quickly_answers
        account_pks = useful_quickly_answers.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='explainer')

    @point_execution_in_terminal
    def check_badge_Refiner(self):
        """Answer on 5 questions within 24 hours and with scope > 0."""
        useful_answers = Answer.objects.answers_by_min_scope(min_scope=1)
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
        account_pks = tuple(item[0] for item in tuple_with_account_pks_and_count_answers)
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='refiner')

    @point_execution_in_terminal
    def check_badge_Illuminator(self):
        """Answer on 10 questions within 24 hours and with scope > 0."""
        useful_answers = Answer.objects.answers_by_min_scope(min_scope=1)
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
        account_pks = tuple(item[0] for item in tuple_with_account_pks_and_count_answers)
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='illuminator')

    @point_execution_in_terminal
    def check_badge_Guru(self):
        """Given accepted answer with score of 5 or more."""
        useful_answers = Answer.objects.answers_by_min_scope(min_scope=5)
        accepted_answers = Answer.objects.accepted_answers()
        good_accepted_answers = useful_answers & accepted_answers
        account_pks = good_accepted_answers.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='guru')

    @point_execution_in_terminal
    def check_badge_Nice_Answer(self):
        """Answer score of 5 or more."""
        answers = Answer.objects.answers_by_min_scope(min_scope=5)
        account_pks = answers.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='nice answer')

    @point_execution_in_terminal
    def check_badge_Good_Answer(self):
        """Answer score of 10 or more."""
        answers = Answer.objects.answers_by_min_scope(min_scope=10)
        account_pks = answers.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='good answer')

    @point_execution_in_terminal
    def check_badge_Great_Answer(self):
        """Answer score of 15 or more."""
        answers = Answer.objects.answers_by_min_scope(min_scope=15)
        account_pks = answers.values_list('author', flat=True).distinct()
        self.added_badge_to_accounts(account_pks=account_pks, badge_name='great answer')

    @point_execution_in_terminal
    def check_badge_Populist(self):
        """Highest scoring answer that outscored an accepted answe."""

    @point_execution_in_terminal
    def check_badge_Reversal(self):
        """Provide an answer of +1 score to a question of -1 score."""
        # Question.objects.

    @point_execution_in_terminal
    def check_badge_Revivel(self):
        """Answer more than 7 days after a question was asked."""
        # Question.objects

    @point_execution_in_terminal
    def check_badge_Necromancer(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_SelfLearner(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Teacher(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Autobiograther(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Commentator(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Sociable(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Enthusiast(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Fanatic(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Assduous(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Epic(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Legendary(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Citize(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Talkative(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Outspoken(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Yearning(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Civic_Duty(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Electorate(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Citizen_Patrol(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Depute(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Marshal(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Critic(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Editor(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Organizer(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Proofreader(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Suffrage(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Vox_Populi(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Supporter(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Taxonomist(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Publicist(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Tester(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Creator_Tests(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Clear_Mind(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Clear_Head(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Closer_Questions(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Deleter_Questions(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Dispatcher(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Sage(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')

    @point_execution_in_terminal
    def check_badge_Have_Opinion(self):
        """ """
        # account_pks = answers.values_list('author', flat=True).distinct()
        # self.added_badge_to_accounts(account_pks=account_pks, badge_name='')
