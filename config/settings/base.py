
import datetime

from django.utils.text import slugify
from django.utils import timezone

from unipath import Path

from mylabour.utils import get_secret_value_for_setting_from_file


# --------------------------------
# CORE SETTINGS
# --------------------------------


BASE_DIR = Path(__file__).ancestor(3)

SITE_ID = 1

SECRET_KEY = get_secret_value_for_setting_from_file(filename='secrets.json', setting_name='SECRET_KEY')

# Application definition

DJANGO_APPS = [
    'suit',
    'django.contrib.admin.apps.SimpleAdminConfig',  # disable auto-discovery
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

MY_APPS = [
    'mylabour',
    'apps.accounts.apps.AccountsConfig',
    'apps.actions.apps.ActionsConfig',
    'apps.articles.apps.ArticlesConfig',
    'apps.badges.apps.BadgesConfig',
    'apps.books.apps.BooksConfig',
    'apps.comments.apps.CommentsConfig',
    'apps.courses.apps.CoursesConfig',
    'apps.favours.apps.FavoursConfig',
    'apps.forum.apps.ForumConfig',
    'apps.inboxes.apps.InboxesConfig',
    'apps.newsletters.apps.NewslettersConfig',
    'apps.opinions.apps.OpinionsConfig',
    'apps.polls.apps.PollsConfig',
    'apps.questions.apps.QuestionsConfig',
    'apps.replies.apps.RepliesConfig',
    'apps.scopes.apps.ScopesConfig',
    'apps.sessions.apps.SessionsConfig',
    'apps.snippets.apps.SnippetsConfig',
    'apps.solutions.apps.SolutionsConfig',
    'apps.tags.apps.TagsConfig',
    'apps.testing.apps.TestingConfig',
    'apps.utilities.apps.UtilitiesConfig',
    'apps.visits.apps.VisitsConfig',
    'apps.web_links.apps.WebLinksConfig',
]

THIRD_PARTY_APPS = [
    'django_cleanup',
    'daterange_filter',
]

INSTALLED_APPS = DJANGO_APPS + MY_APPS + THIRD_PARTY_APPS

# Project settings

DJANGO_MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MY_MIDDLEWARE_CLASSES = [
    'apps.accounts.middleware.LastSeenAccountMiddleware',
    'apps.visits.middleware.CountVisitsPagesMiddleware',
    'apps.visits.middleware.RegistratorVisitAccountMiddleware',
]

MIDDLEWARE_CLASSES = DJANGO_MIDDLEWARE_CLASSES + MY_MIDDLEWARE_CLASSES

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.child('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                # 'django.template.context_processors.tz',
                'mylabour.context_processors.date_creating_website',
                'apps.visits.context_processors.count_visits',
                'apps.sessions.context_processors.users_online',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# -----------------------------
# AUTH
# -----------------------------

AUTH_USER_MODEL = 'accounts.Account'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = '/accounts/login/'

LOGOUT_URL = '/accounts/logout/'

LOGIN_REDIRECT_URL = '/accounts/account_profile/'

PASSWORD_RESET_TIMEOUT_DAYS = 3

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# -----------------------------
# MESSAGES
# -----------------------------

# MESSAGE_LEVEL = 'messages.INFO'

# MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

# MESSAGE_TAGS = {
#     messages.DEBUG: 'debug',
#     messages.INFO: 'info',
#     messages.SUCCESS: 'success',
#     messages.WARNING: 'warning',
#     messages.ERROR: 'error',
# }

# ----------------------------------------
# GLOBALIZATION
# ----------------------------------------

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    BASE_DIR.child('locale'),
)

# FIXTURE_DIRS = (
#     str(APPS_DIR.path('fixtures')),
# )

LAMGUAGES = (
    ('en', 'English'),
    ('ru', 'Russian'),
)

# ----------------------------------------
# STATIC FILES
# ----------------------------------------

STATIC_URL = '/static/'

STATIC_DIRS = [
    BASE_DIR.child('static')
]

STATIC_ROOT = str(BASE_DIR.child('assets'))

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_URL = '/media/'

MEDIA_ROOT = str(BASE_DIR.child('media'))

# ----------------------------------------
# SESSIONS
# ----------------------------------------

SESSION_ENGINE = 'apps.sessions.backends.extended_session_store'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30

SESSION_SERIALIZER = 'apps.sessions.serializers.ComprehensiveSessionJSONSerializer'

# ----------------------------------------
# CACHE
# ----------------------------------------

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'chachetable_for_website',
    }
}

# ----------------------------------------
# MAIL
# ----------------------------------------

ADMINS = [('Seti', 'setivolkylany@gmail.com')]

EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = 'setivolkylany@gmail.com'

EMAIL_HOST_PASSWORD = 'lv210493'

SERVER_EMAIL = 'programmerHelper_admin@gmail.com'

DEFAULT_FROM_EMAIL = 'programmerHelper@gmail.com'


# Third-party app DJANGO_PASSWORD

PASSWORD_MIN_LENGTH = 8

PASSWORD_MAX_LENGTH = 20

PASSWORD_DICTIONARY = None

PASSWORD_MATCH_THRESHOLD = 0.9

# You can omit any or all of these for no limit for that particular set

PASSWORD_COMPLEXITY = {
    # "UPPER": 1,
    # "LOWER": 1,
    "LETTERS": 6,
    "DIGITS": 2,
    "SPECIAL": 0,
    "WORDS": 0,
}


# MY SETTINGS

COUNT_DAYS_DISTINGUISH_ELEMENTS_AS_NEW = 7

MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT = 10

MIN_COUNT_WEBLINKS_ON_OBJECT = 1

MAX_COUNT_WEBLINKS_ON_OBJECT = 10

MIN_COUNT_TAGS_ON_OBJECT = 1

MAX_COUNT_TAGS_ON_OBJECT = 5

DATE_CREATING_WEBSITE = datetime.date(year=2016, month=3, day=1)

IGNORABLE_404_ENDS = ('',)

IGNORABLE_URLS_FOR_COUNT_VISITS = (
    r'admin/[\w]*',
    r'*\.jpeg$',
    r'*\.png$',
    r'*\.jpg$',
    r'*\.gif$',
    r'/favicon.ico$',
    r'/(robots.txt)|(humans.txt)$',
)

AUTOSLUG_SLUGIFY_FUNCTION = lambda value: slugify(value, allow_unicode=True)
