
from django.utils.text import slugify


# Django-Extensions

SHELL_PLUS = 'ipython'

SHELL_PLUS_PRE_IMPORTS = (
    ('django.template', ('Template', 'Context')),
    ('django.contrib', 'admin'),
    ('django.core.management', 'call_command'),
    ('django.apps', 'apps'),
    ('utils', 'django'),
)

SHELL_PLUS_MODEL_ALIASES = {}

SHELL_PLUS_DONT_LOAD = []

SHELL_PLUS_PRINT_SQL = True

IPYTHON_ARGUMENTS = [
    '--ext', 'autoreload',
    # '--no-banner',
    # '--pdb',
    '--pprint',
]


# Django-AutoSlug

AUTOSLUG_SLUGIFY_FUNCTION = lambda value: slugify(value, allow_unicode=True)
