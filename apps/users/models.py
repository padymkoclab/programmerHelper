
import logging
import collections
import itertools
import urllib
import hashlib
import random
import uuid

from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
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
# from django.contrib.auth import password_validation

from utils.django import models_fields as utils_models_fields
from utils.django.models_utils import get_admin_url
from utils.django.functions_db import Round

from apps.tags.models import Tag
# from apps.badges.managers import BadgeManager
from apps.badges.models import Badge
from apps.badges.constants import Badges
# from apps.polls.managers import PollsManager
# from apps.polls.querysets import UserPollQuerySet
# from apps.activity.models import Activity
# from apps.forum.models import Topic
# from apps.sessions.models import ExpandedSession
# from utils.django.models_fields import PhoneField
from apps.polls.models import Poll
from apps.articles.models import Article
from apps.solutions.models import Solution
from apps.utilities.models import Utility
from apps.snippets.models import Snippet
from apps.questions.models import Answer, Question

from .managers import UserManager, LevelManager
from .exceptions import ProtectDeleteUser
from .validators import UsernameValidator


logger = logging.getLogger('django.development')


logger.info('Example user page https://www.digitalocean.com/community/users/jellingwood?primary_filter=upvotes_given')
logger.info('get_chart_visits')
logger.info('get_chart_activity')


def get_favorite_tags(qs_tags_pks):

    if not qs_tags_pks.exists():
        return Tag.objects.none()

    counter_pks_tags = collections.Counter(qs_tags_pks)

    max_counter_pks_tags = max(counter_pks_tags.values())

    filter_max_pks_tags = filter(lambda x: x[1] == max_counter_pks_tags, counter_pks_tags.items())
    pks_tags = dict(filter_max_pks_tags).keys()

    tags = Tag.objects.filter(pk__in=pks_tags)

    return tags


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
    slug = utils_models_fields.ConfiguredAutoSlugField(populate_from='name', unique=True)
    description = models.TextField(
        _('Description'), validators=[MinLengthValidator(10)]
    )
    color = utils_models_fields.ColorField(
        _('Color'), max_length=50,
        help_text=_('Choice color in hex format'),
        unique=True,
        error_messages={'unique': _('Level with color already exists.')}
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
    REQUIRED_FIELDS = ('email', 'alias')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        _('email'), unique=True,
        error_messages={
            'unique': _('User with this email already exists.')
        }
    )
    username = models.CharField(
        _('username'), max_length=40, unique=True,
        error_messages={
            'unique': _('User with this username already exists.')
        },
        validators=[
            MinLengthValidator(3),
            UsernameValidator(),
        ],
        help_text=UsernameValidator.help_text,
    )
    alias = models.CharField(
        _('alias'), max_length=200,
        help_text=_('Name for public display'),
    )
    reputation = models.IntegerField(_('reputation'), default=0, editable=False)
    is_active = models.BooleanField(_('is active?'), default=True)
    level = models.ForeignKey(
        'level',
        verbose_name='Level',
        related_name='users',
        default=Level.REGULAR,
        to_field='name',
    )
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    # managers
    objects = models.Manager()
    objects = UserManager()
    # polls = PollsManager.from_queryset(UserPollQuerySet)()
    # badges_manager = BadgeManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ('-date_joined', )
        get_latest_by = 'date_joined'

    def __str__(self):

        return self.get_short_name()

    def save(self, *args, **kwargs):

        super(User, self).save(*args, **kwargs)

        # auto create
        # self.diary
        # self.profile

    def delete(self, *args, **kwargs):

        # Protect a user from removal, if web application has this restriction
        #
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

    # def clean(self):
    #     pass

    def get_full_name(self):
        """ """

        return '{0.username} ({0.email})'.format(self)
    get_full_name.short_description = Meta.verbose_name
    # get_full_name.admin_order_field = 'username'

    def get_short_name(self):
        return '{0.alias}'.format(self)
    get_short_name.short_description = _('Short name')
    # get_short_name.admin_order_field = 'alias'

    @property
    def is_staff(self):
        return self.is_superuser

    def has_permission(self, perm, obj=None):

        if not self.is_active:
            return False

        if self.is_superuser:
            return True

        return False

    def has_module_permissions(self, label):

        if not self.is_active:
            return False

        if self.is_superuser:
            return True

        return False

    # REQUIRED FOR ALL PROJECTS
    def get_avatar_path(self, size=100, default='identicon'):
        """ """

        gravatar_url = "https://www.gravatar.com/avatar/"
        user_hash = hashlib.md5(self.email.lower().encode()).hexdigest()
        gravatar_parameters = urllib.parse.urlencode({'size': size, 'default': default, 'rating': 'g'})

        return '{}{}?{}'.format(gravatar_url, user_hash, gravatar_parameters)

    # REQUIRED FOR ALL PROJECTS
    def display_avatar(self, size=100):
        """ """

        return format_html('<img src="{}" />', self.get_avatar_path(size))
    display_avatar.short_description = _('Avatar')

    def get_last_seen(self):

        if hasattr(self, 'last_seen'):
            return self.last_seen.date
        return
    get_last_seen.short_description = _('Last seen')
    get_last_seen.admin_order_field = 'last_seen'

    def get_count_days_attendances(self):

        return self.attendances.count()
    get_count_days_attendances.short_description = _('Count days attendance')
    get_count_days_attendances.admin_order_field = 'count_days_attendance'

    def get_total_count_comments(self):
        """ """

        if hasattr(self, 'total_count_comments'):
            return self.total_count_comments

        return self.comments.count()
    get_total_count_comments.short_description = _('Total count comments')
    get_total_count_comments.admin_order_field = 'total_count_comments'

    def get_count_comments_of_articles(self):
        """ """

        if hasattr(self, 'count_comments_articles'):
            return self.count_comments_articles

        ct_model = ContentType.objects.get_for_model(Article)
        return self.comments.filter(content_type=ct_model).count()
    get_count_comments_of_articles.short_description = _('Count comments of articles')
    get_count_comments_of_articles.admin_order_field = 'count_comments_articles'

    def get_count_comments_of_solutions(self):
        """ """

        if hasattr(self, 'count_comments_solutions'):
            return self.count_comments_solutions

        ct_model = ContentType.objects.get_for_model(Solution)
        return self.comments.filter(content_type=ct_model).count()
    get_count_comments_of_solutions.short_description = _('Count comments of solutions')
    get_count_comments_of_solutions.admin_order_field = 'count_comments_solutions'

    def get_count_comments_of_snippets(self):
        """ """

        if hasattr(self, 'count_comments_snippets'):
            return self.count_comments_snippets

        ct_model = ContentType.objects.get_for_model(Snippet)
        return self.comments.filter(content_type=ct_model).count()
    get_count_comments_of_snippets.short_description = _('Count comments of snippets')
    get_count_comments_of_snippets.admin_order_field = 'count_comments_snippets'

    def get_count_comments_of_answers(self):
        """ """

        if hasattr(self, 'count_comments_answers'):
            return self.count_comments_answers

        ct_model = ContentType.objects.get_for_model(Answer)
        return self.comments.filter(content_type=ct_model).count()
    get_count_comments_of_answers.short_description = _('Count comments of answers')
    get_count_comments_of_answers.admin_order_field = 'count_comments_answers'

    def get_count_comments_of_utilities(self):
        """ """

        if hasattr(self, 'count_comments_utilities'):
            return self.count_comments_utilities

        ct_model = ContentType.objects.get_for_model(Utility)
        return self.comments.filter(content_type=ct_model).count()
    get_count_comments_of_utilities.short_description = _('Count comments of utilities')
    get_count_comments_of_utilities.admin_order_field = 'count_comments_utilities'

    def get_date_latest_comment(self):
        """ """

        # if hasattr(self, 'count_comments'):
        #     return self.count_comments

        try:
            return self.comments.latest().created
        except self.comments.model.DoesNotExist:
            return
    get_date_latest_comment.short_description = _('Latest comment')
    get_date_latest_comment.admin_order_field = 'date_latest_comment'

    def get_rating_comments(self):

        logger.critical('Not implemented error')

        return
    get_rating_comments.short_description = _('Rating')
    get_rating_comments.admin_order_field = 'rating'

    def get_date_latest_reply(self):
        """ """

        try:
            return self.replies.latest().created
        except self.replies.model.DoesNotExist:
            return
    get_date_latest_reply.admin_order_field = 'date_latest_reply'
    get_date_latest_reply.short_description = _('Latest reply')

    def get_count_replies(self):
        """ """

        return self.replies.count()
    get_count_replies.admin_order_field = 'count_replies'
    get_count_replies.short_description = _('Count replies')

    def get_total_count_opinions(self):
        """ """

        if hasattr(self, 'total_count_opinions'):
            return self.total_count_opinions

        return self.opinions.count()
    get_total_count_opinions.admin_order_field = 'total_count_opinions'
    get_total_count_opinions.short_description = _('Total count opinions')

    def get_count_opinions_of_solutions(self):

        ct_model = ContentType.objects.get_for_model(Solution)
        return self.opinions.filter(content_type=ct_model).count()
    get_count_opinions_of_solutions.short_description = _('Count opinions of solutions')
    get_count_opinions_of_solutions.admin_order_field = 'count_opinions_solutions'

    def get_count_opinions_of_questions(self):

        ct_model = ContentType.objects.get_for_model(Question)
        return self.opinions.filter(content_type=ct_model).count()
    get_count_opinions_of_questions.short_description = _('Count opinions of questions')
    get_count_opinions_of_questions.admin_order_field = 'count_opinions_questions'

    def get_count_opinions_of_snippets(self):

        ct_model = ContentType.objects.get_for_model(Snippet)
        return self.opinions.filter(content_type=ct_model).count()
    get_count_opinions_of_snippets.short_description = _('Count opinions of snippets')
    get_count_opinions_of_snippets.admin_order_field = 'count_opinions_snippets'

    def get_count_opinions_of_utilities(self):

        ct_model = ContentType.objects.get_for_model(Utility)
        return self.opinions.filter(content_type=ct_model).count()
    get_count_opinions_of_utilities.short_description = _('Count opinions of utilities')
    get_count_opinions_of_utilities.admin_order_field = 'count_opinions_utilities'

    def get_count_opinions_of_answers(self):

        ct_model = ContentType.objects.get_for_model(Answer)
        return self.opinions.filter(content_type=ct_model).count()
    get_count_opinions_of_answers.short_description = _('Count opinions of answers')
    get_count_opinions_of_answers.admin_order_field = 'count_opinions_answers'

    def get_date_latest_opinion(self):
        """ """

        try:
            return self.opinions.latest().created
        except self.opinions.model.DoesNotExist:
            return
    get_date_latest_opinion.admin_order_field = 'date_latest_opinion'
    get_date_latest_opinion.short_description = _('Latest opinion')

    def get_count_marks(self):
        """ """

        if hasattr(self, 'count_marks'):
            return self.count_marks

        return self.marks.count()
    get_count_marks.admin_order_field = 'count_marks'
    get_count_marks.short_description = _('Count marks')

    def get_date_latest_mark(self):
        """ """

        try:
            return self.marks.latest().created
        except self.marks.model.DoesNotExist:
            return
    get_date_latest_mark.admin_order_field = 'date_latest_mark'
    get_date_latest_mark.short_description = _('Latest mark')

    def get_count_questions(self):
        """ """

        if hasattr(self, 'count_questions'):
            return self.count_questions

        return self.questions.count()
    get_count_questions.admin_order_field = 'count_questions'
    get_count_questions.short_description = _('Count questions')

    def get_favorite_tags_of_questions(self):
        """ """

        qs_tags_pks = self.questions.values_list('tags__pk', flat=True)
        favorite_tags = get_favorite_tags(qs_tags_pks)

        return favorite_tags
    get_favorite_tags_of_questions.short_description = _('Favorite tag')

    def get_date_latest_question(self):
        """ """

        # if hasattr(self, 'count_questions'):
        #     return self.count_questions

        try:
            return self.questions.latest().created
        except self.questions.model.DoesNotExist:
            return
    get_date_latest_question.admin_order_field = 'date_latest_question'
    get_date_latest_question.short_description = _('Latest question')

    def get_count_snippets(self):
        """ """

        if hasattr(self, 'count_snippets'):
            return self.count_snippets

        return self.snippets.count()
    get_count_snippets.admin_order_field = 'count_snippets'
    get_count_snippets.short_description = _('Count snippets')

    def get_favorite_tags_of_snippets(self):
        """ """

        qs_tags_pks = self.snippets.values_list('tags__pk', flat=True)
        favorite_tags = get_favorite_tags(qs_tags_pks)

        return favorite_tags
    get_favorite_tags_of_snippets.short_description = _('Favorite tag')

    def get_total_rating_for_snippets(self):
        """ """

        snippets = self.snippets.annotate(rating=models.Sum(models.Case(
            models.When(opinions__is_useful=True, then=1),
            models.When(opinions__is_useful=False, then=-1),
            output_field=models.IntegerField()
        )))

        total_rating = snippets.aggregate(total_rating=Round(models.Avg('rating')))['total_rating']
        return total_rating
    get_total_rating_for_snippets.admin_order_field = 'total_rating'
    get_total_rating_for_snippets.short_description = _('Total rating')

    def get_date_latest_snippet(self):
        """ """

        # if hasattr(self, 'count_snippets'):
        #     return self.count_snippets

        try:
            return self.snippets.latest().created
        except self.snippets.model.DoesNotExist:
            return
    get_date_latest_snippet.admin_order_field = 'date_latest_snippet'
    get_date_latest_snippet.short_description = _('Latest snippet')

    def get_count_solutions(self):
        """ """

        if hasattr(self, 'count_solutions'):
            return self.count_solutions

        return self.solutions.count()
    get_count_solutions.admin_order_field = 'count_solutions'
    get_count_solutions.short_description = _('Count solutions')

    def get_favorite_tags_of_solutions(self):
        """ """

        qs_tags_pks = self.solutions.values_list('tags__pk', flat=True)
        favorite_tags = get_favorite_tags(qs_tags_pks)

        return favorite_tags
    get_favorite_tags_of_solutions.short_description = _('Favorite tag')

    def get_total_rating_for_solutions(self):
        """ """

        solutions = self.solutions.annotate(rating=models.Sum(models.Case(
            models.When(opinions__is_useful=True, then=1),
            models.When(opinions__is_useful=False, then=-1),
            output_field=models.IntegerField()
        )))

        total_rating = solutions.aggregate(total_rating=Round(models.Avg('rating')))['total_rating']
        return total_rating
    get_total_rating_for_solutions.admin_order_field = 'total_rating'
    get_total_rating_for_solutions.short_description = _('Total rating')

    def get_date_latest_solution(self):
        """ """

        # if hasattr(self, 'count_solutions'):
        #     return self.count_solutions

        try:
            return self.solutions.latest().created
        except self.solutions.model.DoesNotExist:
            return
    get_date_latest_solution.admin_order_field = 'date_latest_solution'
    get_date_latest_solution.short_description = _('Latest solution')

    def get_count_articles(self):
        """ """

        if hasattr(self, 'count_articles'):
            return self.count_articles

        return self.articles.count()
    get_count_articles.admin_order_field = 'count_articles'
    get_count_articles.short_description = _('Count article')

    def get_favorite_tags_of_articles(self):
        """ """

        qs_tags_pks = self.articles.values_list('tags__pk', flat=True)
        favorite_tags = get_favorite_tags(qs_tags_pks)

        return favorite_tags
    get_favorite_tags_of_articles.short_description = _('Favorite tag')

    def get_total_rating_for_articles(self):
        """ """

        return self.articles.annotate(
            rating=models.Avg('marks__mark')
        ).aggregate(
            total_rating=Round(models.Avg('rating'))
        )['total_rating']
    get_total_rating_for_articles.admin_order_field = 'total_rating'
    get_total_rating_for_articles.short_description = _('Total rating')

    def get_date_latest_article(self):
        """ """

        # if hasattr(self, 'count_articles'):
        #     return self.count_articles

        try:
            return self.articles.latest().created
        except self.articles.model.DoesNotExist:
            return
    get_date_latest_article.admin_order_field = 'date_latest_article'
    get_date_latest_article.short_description = _('Latest article')

    def get_count_answers(self):
        """ """

        if hasattr(self, 'count_answers'):
            return self.count_answers

        return self.answers.count()
    get_count_answers.admin_order_field = 'count_answers'
    get_count_answers.short_description = _('Count answers')

    def get_favorite_tags_of_answers(self):
        """ """

        qs_tags_pks = self.answers.values_list('question__tags', flat=True)
        favorite_tags = get_favorite_tags(qs_tags_pks)

        return favorite_tags
    get_favorite_tags_of_answers.short_description = _('Favorite tag')

    def get_date_latest_answer(self):
        """ """

        # if hasattr(self, 'count_answers'):
        #     return self.count_answers

        try:
            return self.answers.latest().created
        except self.answers.model.DoesNotExist:
            return
    get_date_latest_answer.admin_order_field = 'date_latest_answer'
    get_date_latest_answer.short_description = _('Latest answer')

    def get_total_rating_for_answers(self):

        answers = self.answers.annotate(rating=models.Sum(models.Case(
            models.When(opinions__is_useful=True, then=1),
            models.When(opinions__is_useful=False, then=-1),
            output_field=models.IntegerField()
        )))

        total_rating = answers.aggregate(total_rating=Round(models.Avg('rating')))['total_rating']
        return total_rating
    get_total_rating_for_answers.short_description = _('Total rating')
    get_total_rating_for_answers.admin_order_field = 'total_rating'

    def get_total_rating_for_questions(self):

        questions = self.questions.annotate(rating=models.Sum(models.Case(
            models.When(opinions__is_useful=True, then=1),
            models.When(opinions__is_useful=False, then=-1),
            output_field=models.IntegerField()
        )))

        total_rating = questions.aggregate(total_rating=Round(models.Avg('rating')))['total_rating']
        return total_rating
    get_total_rating_for_questions.short_description = _('Total rating')
    get_total_rating_for_questions.admin_order_field = 'total_rating'

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

    def get_date_latest_activity_on_forums(self):
        """ """

        date_latest_update_post = self.posts.aggregate(date=models.Max('updated'))['date']
        date_latest_update_topic = self.topics.aggregate(date=models.Max('updated'))['date']

        if date_latest_update_topic is None and date_latest_update_post is None:
            return
        elif date_latest_update_topic is None and date_latest_update_post is not None:
            return date_latest_update_post
        elif date_latest_update_topic is not None and date_latest_update_post is None:
            return date_latest_update_topic
        else:
            return max(date_latest_update_post, date_latest_update_topic)
    get_date_latest_activity_on_forums.admin_order_field = 'date_latest_activity'
    get_date_latest_activity_on_forums.short_description = _('Latest activity')

    def get_count_votes(self):
        """ """

        if hasattr(self, 'count_votes'):
            return self.count_votes

        return self.votes.count()
    get_count_votes.admin_order_field = 'count_votes'
    get_count_votes.short_description = _('Count votes')

    def get_date_latest_vote(self):
        """ """

        try:
            return self.votes.latest().created
        except self.votes.model.DoesNotExist:
            return
    get_date_latest_vote.admin_order_field = 'date_latest_voting'
    get_date_latest_vote.short_description = _('Date of latest voting')

    def is_active_voter(self):
        """ """

        count_polls = Poll._default_manager.count()

        half_count_polls = count_polls // 2

        return self.get_count_votes() > half_count_polls
    is_active_voter.admin_order_field = 'is_active_voter'
    is_active_voter.short_description = _('Is active\nvoter?')
    is_active_voter.boolean = True

    def get_statistics_usage_tags(self, count=None):
        """ """

        raise NotImplementedError

        tags = itertools.chain.from_iterable((
            self.solutions.values_list('tags', flat=True),
            self.snippets.values_list('tags', flat=True),
            self.questions.values_list('tags', flat=True),
            self.articles.values_list('tags', flat=True),
            self.answers.values_list('question__tags', flat=True),
        ))
        tags = collections.Counter(tags).most_common()
        tags = tuple((Tag.objects.get(pk=pk), count) for pk, count in tags)

        if count is not None:
            tags = tuple(tags)[:count]

        return tags

    def _get_couter_pks_usage_tags(self):

        all_tags_pks = itertools.chain.from_iterable((
            self.questions.values_list('tags', flat=True),
            self.snippets.values_list('tags', flat=True),
            self.solutions.values_list('tags', flat=True),
            self.articles.values_list('tags', flat=True),
        ))

        counter = collections.Counter(all_tags_pks)

        return counter

    def get_count_usaged_unique_tags(self):
        """ """

        counter = self._get_couter_pks_usage_tags()
        return len(counter)
    get_count_usaged_unique_tags.short_description = _('Count usaged unique tags')
    get_count_usaged_unique_tags.admin_order_field = 'count_usaged_unique_tags'

    def get_total_count_usaged_tags(self):
        """ """

        counter = self._get_couter_pks_usage_tags()
        return sum(counter.values())
    get_total_count_usaged_tags.short_description = _('Total count usaged tags')
    get_total_count_usaged_tags.admin_order_field = 'total_count_usaged_tags'

    def get_favorite_tags(self):
        """ """

        counter = self._get_couter_pks_usage_tags()

        if len(counter) == 0:
            return

        max_count = counter.most_common(1)[0][1]

        tag_pks = [tag_pk for tag_pk, count in counter.items() if count == max_count]

        return Tag._default_manager.filter(pk__in=tag_pks)
    get_favorite_tags.short_description = _('Favorite tags')

    def have_certain_count_consecutive_days(self, count_consecutive_days):

        raise NotImplementedError

    def get_count_popular_topics(self):
        """Getting count popular topics of user."""
        # popular_topics_of_user = Topic.objects.popular_topics().filter(author=self)

        raise NotImplementedError
        return self.popular_topics_of_user.count()

    def get_reputation(self):
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
        Popular topic                   = 1000 views = + 1

        Vote in poll +1

        ---------------------------------------
        """

        reputation = 0

        total_count_views = self.topics.aggregate(
            total_count_views=models.functions.Coalesce(
                models.Sum('count_views'), 0
            )
        )['total_count_views']
        reputation_for_posts = total_count_views / 1000

        reputation_for_votes = self.get_count_votes()

        values = self.articles.objects_with_rating().values_list('rating', flat=True)
        values = filter(lambda x: x is not None, values)
        reputation_for_articles = sum(values)

        values = self.questions.objects_with_rating().values_list('rating', flat=True)
        values = filter(lambda x: x is not None, values)
        reputation_for_questions = sum(values)

        values = self.snippets.objects_with_rating().values_list('rating', flat=True)
        values = filter(lambda x: x is not None, values)
        reputation_for_snippets = sum(values)

        values = self.solutions.objects_with_rating().values_list('rating', flat=True)
        values = filter(lambda x: x is not None, values)
        reputation_for_solutions = sum(values)

        values = self.answers.objects_with_rating().values_list('rating', flat=True)
        values = filter(lambda x: x is not None, values)
        reputation_for_answers = sum(values)

        reputation = sum((
            reputation_for_posts,
            reputation_for_votes,
            reputation_for_articles,
            reputation_for_questions,
            reputation_for_snippets,
            reputation_for_solutions,
            reputation_for_answers,
        ))

        if self.reputation != round(reputation):

            self.reputation = round(reputation)
            self.full_clean()
            self.save()

        return self.reputation

    def has_badge(self, badge):

        return self.badges.filter(badge=badge).exists()

    def get_count_badges(self):

        return self.badges.count()
    get_count_badges.short_description = _('Count badges')
    get_count_badges.admin_order_field = 'count_badges'

    def get_count_gold_badges(self):

        return self.get_gold_badges().count()
    get_count_gold_badges.short_description = _('Count gold badges')
    get_count_gold_badges.admin_order_field = 'count_gold_badges'

    def get_count_silver_badges(self):

        return self.get_silver_badges().count()
    get_count_silver_badges.short_description = _('Count silver badges')
    get_count_silver_badges.admin_order_field = 'count_silver_badges'

    def get_count_bronze_badges(self):

        return self.get_bronze_badges().count()
    get_count_bronze_badges.short_description = _('Count bronze badges')
    get_count_bronze_badges.admin_order_field = 'count_bronze_badges'

    def get_latest_badge(self):

        try:
            return self.badges.latest()
        except self.badges.model.DoesNotExist:
            return
    get_latest_badge.short_description = _('Latest badge')
    get_latest_badge.admin_order_field = 'latest_badge'

    def get_date_getting_latest_badge(self):

        try:
            return self.badges.latest().date
        except self.badges.model.DoesNotExist:
            return
    get_date_getting_latest_badge.short_description = _('Date getting latest badge')
    get_date_getting_latest_badge.admin_order_field = 'date_latest_badge'

    def get_earned_badges(self):

        return self.badges.all()

    def get_unearned_badges(self):

        return Badge._default_manager.exclude(pk__in=self.badges.all())

    def get_gold_badges(self):

        return self.badges.filter(badge__kind=Badges.Kind.GOLD.value)

    def get_silver_badges(self):

        return self.badges.filter(badge__kind=Badges.Kind.SILVER.value)

    def get_bronze_badges(self):

        return self.badges.filter(badge__kind=Badges.Kind.BRONZE.value)

    def get_notifications(self, by_type='all'):

        if by_type not in ['all', 'read', 'unread']:
            raise ValueError('')

        return self.notifications.order_by('-created')

    def get_count_notifications(self):
        """Count notification send to this user."""

        return 0

        self.get_notifications('all')

        raise NotImplementedError

    def get_count_unread_notifications(self):
        """Count notification send to this user."""

        return 0

        self.get_notifications('all')

        raise NotImplementedError

    def get_count_read_notifications(self):
        """Count notification send to this user."""

        return 0

        self.get_notifications('all')

        raise NotImplementedError


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

    # main fields
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = utils_models_fields.AutoOneToOneField(
        'User', related_name='profile',
        verbose_name=_('User'), on_delete=models.CASCADE
    )

    # public editable info
    about = models.TextField(_('About self'), default='', blank=True)
    signature = models.CharField(_('Signature'), max_length=50, default='', blank=True)
    on_gmail = utils_models_fields.FixedCharField(
        _('Presents on google services'),
        default='', blank=True, max_length=200,
        startswith='https://plus.google.com/u/0/',
    )
    on_github = utils_models_fields.FixedCharField(
        _('Presents on GitHub'),
        default='', blank=True, max_length=200,
        startswith='https://github.com/',
    )
    on_stackoverflow = utils_models_fields.FixedCharField(
        _('Presents on stackoverflow.com'),
        default='', blank=True, max_length=200,
        startswith='https://stackoverflow.com/',
    )
    website = models.URLField(_('Personal website'), default='', blank=True)
    crafts = ArrayField(
        models.CharField(max_length=100),
        size=10, blank=True, null=True,
        verbose_name=_('Directions of development')
    )

    # public noneditable info
    views = models.IntegerField(_('Count views'), default=0, editable=False)

    # private info
    job = models.CharField(
        _('Job'), max_length=100, default='', blank=True,
    )
    gender = models.CharField(
        _('Gender'), max_length=10, choices=CHOICES_GENDER,
        default=UNKNOWN,
    )
    date_birthday = models.DateField(
        _('Date birthday'), null=True, blank=True,
        help_text=_('Only used for displaying age'))
    real_name = models.CharField(_('Real name'), max_length=200, default='', blank=True)
    phone = utils_models_fields.FixedCharField(
        _('Phone'), default='', blank=True, max_length=50,
        startswith='+',
    )

    # user preferences
    show_location = models.BooleanField(_('Show location?'), default=False)
    show_email = models.BooleanField(_('Show email'), default=True)

    # non-editable and hidden information
    latitude = models.FloatField(_('Latitude'), editable=False, null=True)
    longitude = models.FloatField(_('Longitude'), editable=False, null=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return '{}'.format(self.user.get_short_name())

    def get_absolute_url(self):
        return self.user.get_absolute_url()

    def get_admin_url(self):
        return get_admin_url(self)

    def display_location(self):

        template_ = template.Template(" {% load users_tags %}{% display_user_location user height %}")
        context_ = template.Context({
            'user': self,
            'height': 350,
        })
        return template_.render(context=context_)
    display_location.short_description = _('Location')

    def get_percentage_filling(self, with_sign=False):
        """Getting percent filled profile of user."""

        considering_fields = (
            'about',
            'signature',
            'on_gmail',
            'on_github',
            'on_stackoverflow',
            'website',
            'job',
            'date_birthday',
            'real_name',
            'phone',
        )

        result = sum(int(bool(getattr(self, field))) for field in considering_fields)

        if self.gender is not self.UNKNOWN:
            result += 1

        result = result * 100 / len(considering_fields) + 1
        result = round(result, 2)

        if with_sign is True:
            return '{0}%'.format(result)
        return result
    get_percentage_filling.short_description = _('Percentage filling')
    get_percentage_filling.admin_order_field = 'percentage_filling'


# chart reputation
# get_badges_by_sort (silver, bronze, gold)
