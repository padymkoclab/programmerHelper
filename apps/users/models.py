
import logging
import collections
import itertools
import urllib
import hashlib
import random
import uuid

from django.utils.html import format_html
from django.core.validators import MinLengthValidator
from django.utils import timezone
from importlib import import_module
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.conf import settings
from django.core.cache import cache

from utils.django import utils
from utils.django.models_fields import ConfiguredAutoSlugField, PhoneField, AutoOneToOneField, ColorField
from utils.django.models_utils import get_admin_url

from apps.tags.models import Tag
# from apps.polls.managers import PollsManager
# from apps.polls.querysets import UserPollQuerySet
# from apps.articles.models import Article
# from apps.activity.models import Activity
# from apps.forum.models import Topic
# from apps.badges.managers import BadgeManager
# from apps.sessions.models import ExpandedSession
# from utils.django.models_fields import PhoneField

from .managers import UserManager, LevelManager
from .exceptions import ProtectDeleteUser


logger = logging.getLogger('django.development')


class Level(models.Model):
    """

    """

    PLATINUM = 'platinum'
    GOLDEN = 'golden'
    SILVER = 'silver'
    DIAMOND = 'diamond'
    RUBY = 'ruby'
    SAPPHIRE = 'sapphire'
    MALACHITE = 'malachite'
    AMETHYST = 'amethyst'
    EMERALD = 'emerald'
    AGATE = 'agate'
    TURQUOISE = 'turquoise'
    AMBER = 'amber'
    OPAL = 'opal'
    REGULAR = 'regular'

    CHOICES_LEVEL = (
        (PLATINUM, _('Platinum')),
        (GOLDEN, _('Gold')),
        (SILVER, _('Silver')),
        (DIAMOND, _('Diamond')),
        (RUBY, _('Ruby')),
        (SAPPHIRE, _('Sapphire')),
        (MALACHITE, _('Malachite')),
        (AMETHYST, _('Amethyst')),
        (EMERALD, _('Emerald')),
        (AGATE, _('Agate')),
        (TURQUOISE, _('Turquoise')),
        (AMBER, _('Amber')),
        (OPAL, _('Opal')),
        (REGULAR, _('Regular')),
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(
        _('Name'), max_length=50,
        choices=CHOICES_LEVEL, unique=True,
        error_messages={'unique': _('Level with name already exists.')}
    )
    slug = ConfiguredAutoSlugField(populate_from='name', unique=True)
    description = models.TextField(
        _('Description'), validators=[MinLengthValidator(10)]
    )
    color = ColorField(
        _('Color'), max_length=50,
        help_text=_('Enter color name or hex code or rgba'),
    )

    objects = models.Manager()
    objects = LevelManager()

    class Meta:
        verbose_name = _('Level')
        verbose_name_plural = _('Levels')
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()

    def save(self, *args, **kwargs):
        super(Level, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:level', kwargs={'slug': self.slug})

    def get_count_users(self):
        """ """

        if hasattr(self, 'count_users'):
            return self.count_users

        return self.users.count()
    get_count_users.admin_order_field = 'count_users'
    get_count_users.short_description = _('Count users')


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom auth user model with additional fields and username fields as email
    """

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email', 'display_name')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        _('Email'), unique=True,
        error_messages={
            'unique': _('User with this email already exists.')
        }
    )
    username = models.CharField(
        _('Username'), max_length=200, unique=True,
        error_messages={
            'unique': _('User with this username already exists.')
        }
    )
    display_name = models.CharField(
        _('Display name'), max_length=200,
        help_text=_('Name for public display'),
    )
    is_active = models.BooleanField(_('Is active'), default=True)
    level = models.ForeignKey(
        'Level',
        verbose_name='Level',
        related_name='users',
        default=Level.REGULAR,
        to_field='name',
    )
    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True)

    # managers
    objects = models.Manager()
    objects = UserManager()
    # polls = PollsManager.from_queryset(UserPollQuerySet)()
    # badges = BadgeManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ['-date_joined']
        get_latest_by = 'date_joined'

    def __str__(self):
        return self.get_short_name()

    def save(self, *args, **kwargs):

        super(User, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        # Protect a user from removal, if web application has this restriction
        #
        if settings.DEBUG is False:
            if not settings.CAN_DELETE_USER:
                raise ProtectDeleteUser(
                    _(
                        """
                        Sorry, but features our the site not allow removal profile of user.
                        If you want, you can made user as non-active.
                        """
                    )
                )

        super(User, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'email': self.email})

    def get_admin_url(self):
        """ """

        return get_admin_url(self)

    def display_admin_change_link(self):
        """ """

        return format_html('<a href="{}">{}</a>', self.get_admin_url(), self.get_full_name())
    display_admin_change_link.short_description = _('User')

    def get_full_name(self):
        """ """

        return '{0} ({0.email})'.format(self)
    get_full_name.short_description = _('Full name')
    # get_full_name.admin_order_field = 'username'

    def get_short_name(self):
        return '{0.display_name}'.format(self)
    get_short_name.short_description = _('Short name')
    # get_short_name.admin_order_field = 'display_name'

    @property
    def is_staff(self):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, label):
        return True

    # def last_seen(self):
    #     last_session_of_user = ExpandedSession.objects.filter(user_pk=self.pk).order_by('expire_date').last()
    #     if last_session_of_user:
    #         SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
    #         session = SessionStore(session_key=last_session_of_user.session_key)
    #         last_seen = session['last_seen']
    #         return last_seen
    #     return None

    def has_diary(self):

        return hasattr(self, 'diary')
    has_diary.short_description = _('Has diary?')
    has_diary.boolean = True

    def get_gavatar_url(self, size=100, default='identicon'):
        """ """

        gravatar_url = "https://www.gravatar.com/avatar/"
        user_hash = hashlib.md5(self.email.lower().encode()).hexdigest()
        gravatar_parameters = urllib.parse.urlencode({'size': size, 'default': default, 'rating': 'g'})

        return '{}{}?{}'.format(gravatar_url, user_hash, gravatar_parameters)

    def display_avatar(self, size=100):
        """ """

        return format_html('<img src="{}" />', self.get_gavatar_url(size))
    display_avatar.short_description = _('Avatar')

    @property
    def last_seen(self):
        """ """

        return 'ERROR'

    def get_count_comments(self):
        """ """

        if hasattr(self, 'count_comments'):
            return self.count_comments

        return self.comments.count()
    get_count_comments.admin_order_field = 'count_comments'
    get_count_comments.short_description = _('Count comments')

    def get_count_opinions(self):
        """ """

        if hasattr(self, 'count_opinions'):
            return self.count_opinions

        return self.opinions.count()
    get_count_opinions.admin_order_field = 'count_opinions'
    get_count_opinions.short_description = _('Count opinions')

    def get_count_likes(self):
        """ """

        if hasattr(self, 'count_likes'):
            return self.count_likes

        return self.likes.count()
    get_count_likes.admin_order_field = 'count_likes'
    get_count_likes.short_description = _('Count likes')

    def get_count_marks(self):
        """ """

        if hasattr(self, 'count_marks'):
            return self.count_marks

        return self.marks.count()
    get_count_marks.admin_order_field = 'count_marks'
    get_count_marks.short_description = _('Count marks')

    def get_count_questions(self):
        """ """

        if hasattr(self, 'count_questions'):
            return self.count_questions

        return self.questions.count()
    get_count_questions.admin_order_field = 'count_questions'
    get_count_questions.short_description = _('Count questions')

    def get_count_snippets(self):
        """ """

        if hasattr(self, 'count_snippets'):
            return self.count_snippets

        return self.snippets.count()
    get_count_snippets.admin_order_field = 'count_snippets'
    get_count_snippets.short_description = _('Count snippets')

    def get_count_articles(self):
        """ """

        if hasattr(self, 'count_articles'):
            return self.count_articles

        return self.articles.count()
    get_count_articles.admin_order_field = 'count_articles'
    get_count_articles.short_description = _('Count article')

    def get_count_answers(self):
        """ """

        if hasattr(self, 'count_answers'):
            return self.count_answers

        return self.answers.count()
    get_count_answers.admin_order_field = 'count_answers'
    get_count_answers.short_description = _('Count answers')

    def get_count_solutions(self):
        """ """

        if hasattr(self, 'count_solutions'):
            return self.count_solutions

        return self.solutions.count()
    get_count_solutions.admin_order_field = 'count_solutions'
    get_count_solutions.short_description = _('Count solutions')

    def get_count_posts(self):
        """ """

        if hasattr(self, 'count_posts'):
            return self.count_posts

        return self.posts.count()
    get_count_posts.admin_order_field = 'count_posts'
    get_count_posts.short_description = _('Count posts')

    def get_count_topics(self):
        """ """

        if hasattr(self, 'count_topics'):
            return self.count_topics

        return self.topics.count()
    get_count_topics.admin_order_field = 'count_topics'
    get_count_topics.short_description = _('Count topics')

    def get_count_test_suits(self):
        """ """

        if hasattr(self, 'count_test_suits'):
            return self.count_test_suits

        return self.test_suits.count()
    get_count_test_suits.admin_order_field = 'count_test_suits'
    get_count_test_suits.short_description = _('Count test suits')

    def get_count_passages(self):
        """ """

        if hasattr(self, 'count_passages'):
            return self.count_passages

        return self.passages.count()
    get_count_passages.admin_order_field = 'count_passages'
    get_count_passages.short_description = _('Count passages')

    def get_count_votes(self):
        """ """

        if hasattr(self, 'count_votes'):
            return self.count_votes

        return self.votes.count()
    get_count_votes.admin_order_field = 'count_votes'
    get_count_votes.short_description = _('Count votes')

    def get_date_latest_voting(self, obj):
        return obj.date_latest_voting
    get_date_latest_voting.admin_order_field = 'date_latest_voting'
    get_date_latest_voting.short_description = _('Date of latest voting')

    def is_active_voter(self, obj):
        return obj.is_active_voter
    is_active_voter.admin_order_field = 'is_active_voter'
    is_active_voter.short_description = _('Is active\nvoter?')
    is_active_voter.boolean = True

    def get_statistics_usage_tags(self):
        """ """

        tags = itertools.chain.from_iterable((
            self.solutions.values_list('tags', flat=True),
            self.snippets.values_list('tags', flat=True),
            self.questions.values_list('tags', flat=True),
            self.articles.values_list('tags', flat=True),
            self.answers.values_list('question__tags', flat=True),
        ))
        tags = collections.Counter(tags).most_common()
        tags = ((Tag.objects.get(pk=pk), count) for pk, count in tags)

        return tuple(tags)

    def have_certain_count_consecutive_days(self, count_consecutive_days):
        if count_consecutive_days > 0:
            if count_consecutive_days <= self.days_attendances.count():
                list_all_dates = self.days_attendances.only('day_attendance').values_list('day_attendance', flat=True)
                # getting differents between dates as timedelta objects
                differents_dates = utils.get_different_between_elements(sequence=list_all_dates, left_to_right=False)
                # converting timedelta objects in numbers
                differents_dates = tuple(timedelta.days for timedelta in differents_dates)
                # find the groups consecutive elements
                groups_concecutive_elements = utils.show_concecutive_certain_element(differents_dates, 1)
                # determinate max count consecutive elements
                max_count_concecutive_elements = max(len(group) for group in groups_concecutive_elements)
                # add 1 for учитывания первого дня
                max_count_concecutive_elements = max_count_concecutive_elements + 1 if max_count_concecutive_elements else 0
                if 0 < count_consecutive_days <= max_count_concecutive_elements:
                    return True
            return False
        raise ValueError('Count consecutive days must be 1 or more,')

    # def activity_with_users(self):
    #     return self.activity.filter(flag=Activity.CHOICES_FLAGS.profiling).all()

    def check_badge(self, badge_name):
        instance = self._as_queryset()
        return self.__class__.badges_manager.validate_badges(users=instance, badges_names=[badge_name])

    def has_badge(self, badge_name):
        return self.__class__.badges_manager.has_badge(user=self, badge_name=badge_name)

    @property
    def reputation(self):
        return self.get_reputation()

    def get_reputation(self):
        """Getting reputation 1of user based on his activity, activity, badges."""

        return 'ERROR'

        return sum([
            self.get_reputation_for_badges(),
            self.get_reputation_for_activity(),
        ])
    get_reputation.short_description = _('Reputation')

    def get_reputation_for_badges(self):
        """Getting reputation of user for badges."""
        return self.badges.count() * 10

    def get_total_mark_for_answers(self):
        """Getting total mark for answers of user."""
        # getting instance as queryset
        queryset = self.__class__.objects.filter(email=self.email)
        # pass single queryset for execution once iteration in method of manager
        user_with_total_mark_for_answers = self.__class__.objects.users_with_total_mark_for_answers(queryset=queryset)
        # getting back instance after processing
        user_with_total_mark_for_answers = user_with_total_mark_for_answers.get()
        # return total_mark_for_answers of instance
        return user_with_total_mark_for_answers.total_mark_for_answers

    def get_total_mark_for_questions(self):
        """Getting total mark for questions of user."""
        # getting instance as queryset
        queryset = self.__class__.objects.filter(email=self.email)
        # pass single queryset for execution once iteration in method of manager
        user_with_total_mark_for_questions = self.__class__.objects.users_with_total_mark_for_questions(queryset=queryset)
        # getting back instance after processing
        user_with_total_mark_for_questions = user_with_total_mark_for_questions.get()
        # return total_mark_for_questions of instance
        return user_with_total_mark_for_questions.total_mark_for_questions

    def get_total_mark_for_solutions(self):
        """Getting total mark for solutions of user."""
        # getting instance as queryset
        queryset = self.__class__.objects.filter(email=self.email)
        # pass single queryset for execution once iteration in method of manager
        user_with_total_mark_for_solutions = self.__class__.objects.users_with_total_mark_for_solutions(queryset=queryset)
        # getting back instance after processing
        user_with_total_mark_for_solutions = user_with_total_mark_for_solutions.get()
        # return total_mark_for_solutions of instance
        return user_with_total_mark_for_solutions.total_mark_for_solutions

    def get_total_mark_for_snippets(self):
        """Getting total mark for snippets of user."""
        # getting instance as queryset
        queryset = self.__class__.objects.filter(email=self.email)
        # pass single queryset for execution once iteration in method of manager
        user_with_total_mark_for_snippets = self.__class__.objects.users_with_total_mark_for_snippets(queryset=queryset)
        # getting back instance after processing
        user_with_total_mark_for_snippets = user_with_total_mark_for_snippets.get()
        # return total_mark_for_snippets of instance
        return user_with_total_mark_for_snippets.total_mark_for_snippets

    def get_total_rating_for_articles(self):
        """Getting total ratings of all articles of user."""
        evaluation_total_rating_for_articles_of_user = Article.objects.articles_with_rating().filter(author=self).aggregate(
            total_rating_for_articles=models.Sum('rating')
        )
        # return 0 if user not have articles
        total_rating_for_articles = evaluation_total_rating_for_articles_of_user['total_rating_for_articles'] or 0
        return total_rating_for_articles
        # 3.8
        # фотийодинцова@hotmail.com

    def get_count_popular_topics(self):
        """Getting count popular topics of user."""
        # popular_topics_of_user = Topic.objects.popular_topics().filter(author=self)
        return popular_topics_of_user.count()

    def get_count_testing_suits_in_which_user_involed(self):
        """In creating, how many testing suit involved user."""
        return self.testing_suits.count()

    def get_count_courses_in_which_user_involed(self):
        """In creating, how many testSuit involved user."""
        return self.courses.count()

    def get_reputation_for_activity(self):
        """
        Getting reputation of user for activity on website:
        marks of published snippets, answers, questions and rating of articles,
        participate in polls.
        ---------------------------------------
            Evaluate reputation for activity
        ---------------------------------------
        Mark answers                   = *2
        Mark questions                 = *1
        Mark solutions                 = *3
        Rating articles                 = *4
        Mark snippets                  = *2
        Filled profile                  = *1
        Participate in poll             = *1
        Popular topic                   = *100
        Participate in creating tests   = *100
        Participate in creating courses = *200
        ---------------------------------------
        """
        reputation_for_snippets = (self.get_total_mark_for_snippets() or 0) * 2
        reputation_for_solutions = (self.get_total_mark_for_solutions() or 0) * 3
        reputation_for_questions = (self.get_total_mark_for_questions() or 0) * 1
        reputation_for_answers = (self.get_total_mark_for_answers() or 0) * 2
        # reputation_for_polls = self.get_count_participate_in_polls() or 0
        reputation_for_filled_user_profile = self.get_percent_filled_user_profile() or 0
        # reputation_for_polls = (self.get_total_rating_for_articles() or 0) * 4
        # reputation_for_polls = (self.get_count_popular_topics() or 0) * 100
        reputation_for_test_suits = (self.get_count_testing_suits_in_which_user_involed() or 0) * 100
        reputation_for_courses = (self.get_count_courses_in_which_user_involed() or 0) * 200
        return sum([
            reputation_for_snippets,
            reputation_for_solutions,
            reputation_for_questions,
            reputation_for_answers,
            # reputation_for_polls,
            reputation_for_filled_user_profile,
            # reputation_for_polls,
            # reputation_for_polls,
            reputation_for_test_suits,
            reputation_for_courses,
        ])

    def get_top_tags(self):
        """Return dict as couple: 'tag': percent_usage % """

        return NotImplementedError

    def comments(self):

        return NotImplementedError

    def count_comments(self):

        return NotImplementedError

    # https://www.digitalocean.com/community/users/jellingwood?primary_filter=upvotes_given
    # answer, queations, hearts, opinons and more
    #


class Profile(models.Model):
    """

    """

    MAN = 'MAN'
    WOMAN = 'WOMAN'
    UNKNOWN = 'UNKNOWN'

    CHOICES_GENDER = (
        (MAN, _('Man')),
        (WOMAN, _('Woman')),
        (UNKNOWN, _('Unknown'))
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = AutoOneToOneField(
        'User', related_name='profile',
        verbose_name=_('User'), on_delete=models.CASCADE
    )

    # public info
    views = models.IntegerField(_('Count views'), default=0, editable=False)

    # crafts = models.CharField() ваши направления развития верстка, программирование
    # theme of site

    about = models.TextField(_('About self'), default='', blank=True)
    signature = models.CharField(_('Signature'), max_length=50, default='', blank=True)
    presents_on_gmail = models.URLField(_('Presents on google services'), default='', blank=True)
    presents_on_github = models.URLField(_('Presents on GitHub'), default='', blank=True)
    presents_on_stackoverflow = models.URLField(_('Presents on stackoverflow.com'), default='', blank=True)
    personal_website = models.URLField(_('Personal website'), default='', blank=True)
    gender = models.CharField(
        _('Gender'), max_length=10, choices=CHOICES_GENDER,
        default=UNKNOWN,
    )
    job = models.CharField(
        _('Job'), max_length=100, default='', blank=True,
    )

    location = models.CharField(_('Location'), max_length=50, default='', blank=True)
    latitude = models.FloatField(_('Latitude'), blank=True, null=True)
    longitude = models.FloatField(_('Longitude'), blank=True, null=True)

    # show_email = models.BooleanField(_('Show email'), default=True)

    # private info
    date_birthday = models.DateField(
        _('Date birthday'), null=True, blank=True,
        help_text=_('Only used for displaying age'))
    real_name = models.CharField(_('Real name'), max_length=200, default='', blank=True)
    phone = PhoneField(_('Phone'), default='', blank=True)

    updated = models.DateTimeField(_('Updated'), auto_now=True)

    def __str__(self):
        return '{}'.format(self.user.get_short_name())

    def get_absolute_url(self):
        return self.user.get_absolute_url()

    def get_admin_url(self):
        return get_admin_url(self)

    @property
    def last_seen(self):

        key = 'LastSeenUser{}'.format(self.user.pk)
        date_last_seen = cache.get(key)

        if date_last_seen is not None:
            return date_last_seen
        return

    def get_percentage_filling(self):
        """Getting percent filled profile of user."""

        logger.error('Not correct and untested results')
        logger.error('Does not work "admin_order_field"')

        considering_fields = (
            'about',
            'signature',
            'presents_on_gmail',
            'presents_on_github',
            'presents_on_stackoverflow',
            'personal_website',
            'job',
            'location',
            'latitude',
            'longitude',
            'date_birthday',
            'real_name',
            'phone',
        )

        result = sum(int(bool(getattr(self, field))) for field in considering_fields)

        if self.gender is not self.UNKNOWN:
            result += 1

        result = result * 100 / len(considering_fields) + 1
        result = round(result, 2)

        return '{0}%'.format(result)
    get_percentage_filling.short_description = _('Percentage filling')
    get_percentage_filling.admin_order_field = 'percentage_filling'


# get_top_tag
# chart reputation
# get_badges_by_sort (silver, bronze, gold)


# class Notification(models.Model):
#     """ """

#     CHOICES_NOTIFICATIONS = (
#         (_('Message')),
#         (_('Comment')),
#         (_('Badge')),
#         (_('Reputation')),
#     )

#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     type = models.CharField(_('Type'), max_length=50, choices=CHOICES_NOTIFICATIONS)
#     user = models.ForeignKey(
#         'User', related_name='notifications',
#         verbose_name=_('User'), on_delete=models.CASCADE
#     )
#     content = models.CharField(_('Content'), max_length=300)
#     created = models.DateTimeField(_('Created'), auto_now_add=True)
