
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
        self.check_badge_Favorite_Question(account=None)
        self.check_badge_Stellar_Question(account=None)
        self.check_badge_Nice_Question(account=None)
        self.check_badge_Good_Question(account=None)
        self.check_badge_Great_Question(account=None)
        self.check_badge_Popular_Question(account=None)
        self.check_badge_Notable_Question(account=None)
        self.check_badge_Famous_Question(account=None)
        self.check_badge_Schoolar(account=None)
        self.check_badge_Student(account=None)
        self.check_badge_Tumbleweed(account=None)
        self.check_badge_Enlightened(account=None)
        # print(']', end='')

    def has_badge(self, account, badge):
        """Checkup presence badges in account"""
        try:
            GettingBadge.objects.get(account=account, badge=badge)
        except GettingBadge.DoesNotExist:
            return False
        else:
            return True

    def last_got_badges(self, count=10):
        return GettingBadge.objects.order_by('-date_getting')[:count]

    def added_badge_to_account(self, account, badge_name):
        badge = Badge.objects.get(name__icontains=badge_name)
        GettingBadge.objects.update_or_create(user=account, badge=badge)

    @point_execution_in_terminal
    def check_badge_Favorite_Question(self, account):
        """Question if favorited at least 5 users."""
        QUESTION_AS_FAVORITE = 5
        for account in self.iterator():
            scopes_questions = account.get_questions_of_account_with_count_favorites_this_questions()
            result = tuple(filter(lambda item: item[1] >= QUESTION_AS_FAVORITE, scopes_questions.items()))
            if result:
                self.added_badge_to_account(account=account, badge_name='favorite question')

    @point_execution_in_terminal
    def check_badge_Stellar_Question(self, account):
        """Question if favorited at least 10 users."""
        QUESTION_AS_STELLAR = 10
        for account in self.iterator():
            scopes_questions = account.get_questions_of_account_with_count_favorites_this_questions()
            result = tuple(filter(lambda item: item[1] >= QUESTION_AS_STELLAR, scopes_questions.items()))
            if result:
                self.added_badge_to_account(account=account, badge_name='stellar question')

    @point_execution_in_terminal
    def check_badge_Nice_Question(self, account):
        """Scope of question must be 5 and more."""
        SCOPES_QUESTION_AS_NICE = 5
        for account in self.iterator():
            scopes_questions = account.get_scopes_questions_of_account()
            result = tuple(filter(lambda item: item[1] >= SCOPES_QUESTION_AS_NICE, scopes_questions.items()))
            if result:
                self.added_badge_to_account(account=account, badge_name='nice question')

    @point_execution_in_terminal
    def check_badge_Good_Question(self, account):
        """Scope of question must be 10 and more."""
        SCOPES_QUESTION_AS_GOOD = 10
        for account in self.iterator():
            scopes_questions = account.get_scopes_questions_of_account()
            result = tuple(filter(lambda item: item[1] >= SCOPES_QUESTION_AS_GOOD, scopes_questions.items()))
            if result:
                self.added_badge_to_account(account=account, badge_name='good question')

    @point_execution_in_terminal
    def check_badge_Great_Question(self, account):
        """Scope of question must be 20 and more."""
        SCOPES_QUESTION_AS_GREAT = 20
        for account in self.iterator():
            scopes_questions = account.get_scopes_questions_of_account()
            result = tuple(filter(lambda item: item[1] >= SCOPES_QUESTION_AS_GREAT, scopes_questions.items()))
            if result:
                self.added_badge_to_account(account=account, badge_name='great question')

    @point_execution_in_terminal
    def check_badge_Popular_Question(self, account):
        """Count views of question must be 100 and more."""
        COUNT_VIEWS_QUESTION_AS_POPULAR = 100
        for account in self.iterator():
            if account.questions.filter(views__gte=COUNT_VIEWS_QUESTION_AS_POPULAR).exists():
                self.added_badge_to_account(account=account, badge_name='popular question')

    @point_execution_in_terminal
    def check_badge_Notable_Question(self, account):
        """Count views of question must be 100 and more."""
        COUNT_VIEWS_QUESTION_AS_NOTABLE = 500
        for account in self.iterator():
            if account.questions.filter(views__gte=COUNT_VIEWS_QUESTION_AS_NOTABLE).exists():
                self.added_badge_to_account(account=account, badge_name='notable question')

    @point_execution_in_terminal
    def check_badge_Famous_Question(self, account):
        """Count views of question must be 1000 and more."""
        COUNT_VIEWS_QUESTION_AS_FAMOUS = 1000
        for account in self.iterator():
            if account.questions.filter(views__gte=COUNT_VIEWS_QUESTION_AS_FAMOUS).exists():
                self.added_badge_to_account(account=account, badge_name='famous question')

    @point_execution_in_terminal
    def check_badge_Schoolar(self, account):
        """Have question with acceptabled answer."""
        for account in self.iterator():
            for question in account.questions.iterator():
                if question.has_acceptabled_answer():
                    self.added_badge_to_account(account=account, badge_name='schoolar')
                    break

    @point_execution_in_terminal
    def check_badge_Student(self, account):
        """Accept an answers on 5 questions."""
        NECESSARY_COUNT_ACCEPT_ANSWERS = 5
        questions_with_acceptabled_answer = frozenset(Question.questions_with_acceptabled_answer.all())
        for account in self.iterator():
            common_questions_with_acceptabled_answer = questions_with_acceptabled_answer & frozenset(account.questions.all())
            if len(common_questions_with_acceptabled_answer) >= NECESSARY_COUNT_ACCEPT_ANSWERS:
                self.added_badge_to_account(account=account, badge_name='student')

    @point_execution_in_terminal
    def check_badge_Tumbleweed(self, account):
        """Asked a question with zero score or less, no answers."""
        non_interesting_questions = frozenset(Question.objects.non_interesting_questions())
        for account in self.iterator():
            if non_interesting_questions & frozenset(account.questions.all()):
                self.added_badge_to_account(account=account, badge_name='tumbleweed')

    @point_execution_in_terminal
    def check_badge_Enlightened(self, account):
        """Had accepted answer with score of 10 or more."""
        good_answers = frozenset(Answer.objects.good_answers())
        for account in self.iterator():
            if good_answers & frozenset(account.answers.all()):
                self.added_badge_to_account(account=account, badge_name='enlightened')

    # Explainer
    # Refiner
    # Illuminator
    # Guru
    # Nice answer
    # Good answer
    # Great answer
    # Populist
    # Reversal
    # Revival
    # Necromancer
    # Self-learner
    # Teacher
    # Autobiograther
    # Commentator
    # Sociable
    # Enthusiast
    # Fanatic
    # Assduous
    # Epic
    # Legendary
    # Citize
    # Talkative
    # Outspoken
    # Yearning
    # Civic Duty
    # Electorate
    # Citizen Patrol
    # Depute
    # Marshal
    # Critic
    # Editor
    # Organizer
    # Proofreader
    # Suffrage
    # Vox populi
    # Supporter
    # Taxonomist
    # Publicist
    # Tester
    # Creator tests
    # Clear mind
    # Clear head
    # Closer questions
    # Deleter questions
    # Dispatcher
    # Sage
    # Have opinion

