
from unipath import Path

from utils.django.utils import get_secret_value_for_setting_from_file

from .custom import *
from .thirdparty import *


BASE_DIR = Path(__file__).ancestor(3)

SITE_ID = 1

SECRET_KEY = get_secret_value_for_setting_from_file(filename='secrets.json', setting_name='SECRET_KEY')

# Application definition

DJANGO_APPS = [
    # 'django.contrib.admin.apps.SimpleAdminConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    # 'django_js_reverse',
    # 'django_gravatar',
    'suit_ckeditor',
]

COMMON_APPS = [
    'utils.django',
    'apps.core.apps.CoreConfig',
    'apps.export_import_models.apps.ExportImportModelsConfig',
    'apps.sessions.apps.SessionsConfig',
]

CUSTOM_APPS = [
    'apps.activity.apps.ActivityConfig',
    'apps.articles.apps.ArticlesConfig',
    'apps.badges.apps.BadgesConfig',
    'apps.books.apps.BooksConfig',
    'apps.comments.apps.CommentsConfig',
    # 'apps.courses.apps.CoursesConfig',  # temporary is disabled
    'apps.flavours.apps.FlavoursConfig',
    'apps.forum.apps.ForumConfig',
    'apps.marks.apps.MarksConfig',
    'apps.newsletters.apps.NewslettersConfig',
    'apps.notifications.apps.NotificationsConfig',
    'apps.opinions.apps.OpinionsConfig',
    'apps.polls.apps.PollsConfig',
    'apps.questions.apps.QuestionsConfig',
    'apps.replies.apps.RepliesConfig',
    'apps.snippets.apps.SnippetsConfig',
    'apps.solutions.apps.SolutionsConfig',
    'apps.tags.apps.TagsConfig',
    'apps.testing.apps.TestingConfig',
    'apps.users.apps.UsersConfig',
    'apps.utilities.apps.UtilitiesConfig',
    'apps.visits.apps.VisitsConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + COMMON_APPS + CUSTOM_APPS
INSTALLED_APPS.insert(0, 'suit')

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
    # 'utils.middleware.TimeLoadPageMiddleware',
    # 'utils.middleware.CountQueriesMiddleware',
    # 'apps.visits.middleware.CountVisitsPageMiddleware',
    # 'apps.visits.middleware.RegistratorVisitAccountMiddleware',
]

MIDDLEWARE = DJANGO_MIDDLEWARE_CLASSES + MY_MIDDLEWARE_CLASSES

ROOT_URLCONF = 'apps.core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.child('templates')
        ],
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
                # 'django.core.context_processors.request',
                # 'django.template.context_processors.tz',
            ],
        },
    },
]

MY_CONTEXT_PROCCESSORS = [
    # 'utils.context_processors.date_creating_website',
    # 'apps.visits.context_processors.count_visits',
    # 'apps.sessions.context_processors.users_online',
]

TEMPLATES[0]['OPTIONS']['context_processors'].extend(MY_CONTEXT_PROCCESSORS)

WSGI_APPLICATION = 'config.wsgi.application'


# -----------------------------
# AUTH
# -----------------------------

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = '/users/login/'

LOGOUT_URL = '/users/logout/'

LOGIN_REDIRECT_URL = '/users/profile/'

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s'
        },
        'django.development': {
            'format': '%(name)s - %(module)s - %(message)s',
        }
    },
    'handlers': {
        'django.development': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'django.development',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'level': 'INFO'
        },
        'django.server': {
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
            'level': 'INFO'
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'level': 'ERROR'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO'
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False
        },
        'django.development': {
            'handlers': ['django.development'],
            'level': 'DEBUG',
            'propagate': False
        },
    },
}


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

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    BASE_DIR.child('locale'),
)

FIXTURE_DIRS = (
    str(BASE_DIR.child('fixtures')),
)

LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Russian'),
)

# ----------------------------------------
# STATIC FILES
# ----------------------------------------

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR.child('static'),
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
        'LOCATION': 'chachetable',
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

# ----------------------------------------
# GEOIP2
# ----------------------------------------

GEOIP_PATH = str(BASE_DIR.child('static', 'project', 'files'))

# SERIALIZERS

SERIALIZATION_MODULES = {'csv': 'apps.export_import_models.serializers.csv'}
