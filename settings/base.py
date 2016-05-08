
from django.utils.text import slugify

from unipath import Path

from mylabour.utils import get_secret_value_for_setting_from_file

# Basic settings

BASE_DIR = Path(__file__).ancestor(2)

SITE_ID = 1

SECRET_KEY = get_secret_value_for_setting_from_file(filename='secrets.json', setting_name='SECRET_KEY')

# Application definition

DJANGO_APPS = [
    'suit',
    'django.contrib.admin.apps.SimpleAdminConfig',  # disable auto-discovery
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MY_APPS = [
    'mylabour',
    'apps.app_accounts.apps.AppAccountsConfig',
    'apps.app_badges.apps.AppBadgesConfig',
    'apps.app_programming_tester.apps.AppProgrammingTesterConfig',
    'apps.app_programming_utilities.apps.AppProgrammingUtilitiesConfig',
    'apps.app_web_links.apps.AppWebLinksConfig',
    'apps.app_articles.apps.AppArticlesConfig',
    'apps.app_solutions.apps.AppSolutionsConfig',
    'apps.app_tags.apps.AppTagsConfig',
    'apps.app_books.apps.AppBooksConfig',
    'apps.app_forum.apps.AppForumConfig',
    'apps.app_snippets.apps.AppSnippetsConfig',
    'apps.app_newsletters.apps.AppNewslettersConfig',
    'apps.app_cources.apps.AppCourcesConfig',
    'apps.app_polls.apps.AppPollsConfig',
    'apps.app_questions.apps.AppQuestionsConfig',
    'apps.app_generic_models.apps.AppGenericModelsConfig',
]

THIRD_PARTY_APPS = [
    'django_cleanup',
]

INSTALLED_APPS = DJANGO_APPS + MY_APPS + THIRD_PARTY_APPS


# Project settings

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project_programmerHelper.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'project_programmerHelper.wsgi.application'


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


# Internationalization

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    BASE_DIR.child('locale'),
)

LAMGUAGES = (
    ('en', 'English'),
    ('ru', 'Russian'),
)


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATIC_DIRS = [
    BASE_DIR.child('static')
]

STATIC_ROOT = BASE_DIR.child('assets')

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR.child('media')

# Mail

ADMINS = [('Seti', 'setivolkylany@gmail.com')]

EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = 'setivolkylany@gmail.com'

EMAIL_HOST_PASSWORD = 'lv210493'

SERVER_EMAIL = 'programmerHelper_admin@gmail.com'

DEFAULT_FROM_EMAIL = 'programmerHelper@gmail.com'

# Auth

AUTH_USER_MODEL = 'app_accounts.Account'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = '/accounts/login/'

LOGOUT_URL = '/accounts/logout/'

LOGIN_REDIRECT_URL = '/accounts/account_profile/'

PASSWORD_RESET_TIMEOUT_DAYS = 3


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


# APPS settings

COUNT_DAYS_DISTINGUISH_ELEMENTS_AS_NEW = 7

MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT = 10

MAX_COUNT_WEBLINKS_ON_OBJECT = 10

MIN_COUNT_TAGS_ON_OBJECT = 1

MAX_COUNT_TAGS_ON_OBJECT = 5

AUTOSLUG_SLUGIFY_FUNCTION = lambda value: slugify(value, allow_unicode=True).replace('-', '_')
