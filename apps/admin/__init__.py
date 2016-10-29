
# from .site import DefaultSiteAdmin
# from .admin import ModelAdmin, StackedInline, TabularInline
# from .app import AppAdmin
from .utils import (
    autodiscover_modules,
    # register_app, register_model
)


__all__ = [
    'DefaultSiteAdmin', 'AppAdmin', 'ModelAdmin', 'StackedInline', 'TabularInline',
    'register_app', 'register_model'
]


def autodiscover():

    autodiscover_modules('admin')
