
from django.utils.text import slugify


# Django-Extensions

SHELL_PLUS = 'ipython'

# additional autoload
SHELL_PLUS_PRE_IMPORTS = (
    ('django.template', ('Template', 'Context')),
    ('django.contrib', 'admin'),
    ('django.core.management', 'call_command'),
    ('django.apps', 'apps'),
    ('utils', 'django'),
)

# what needn`t rename in time autoload
SHELL_PLUS_MODEL_ALIASES = {
    # 'accounts': {'Account': 'AAAA'},
}

# what needn`t autoload
SHELL_PLUS_DONT_LOAD = [
    # '',  # app name
]

SHELL_PLUS_PRINT_SQL = True

IPYTHON_ARGUMENTS = [
    # '--ext', '',
    '--no-banner',
    '--pdb',
    '--pprint',
]


# Django-AutoSlug

AUTOSLUG_SLUGIFY_FUNCTION = lambda value: slugify(value, allow_unicode=True)
