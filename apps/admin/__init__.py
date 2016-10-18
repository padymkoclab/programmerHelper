
# from .site import DefaultSiteAdmin
# from .admin import ModelAdmin
# from .app import AppAdmin
from .utils import autodiscover_modules


__all__ = ['DefaultSiteAdmin', 'AppAdmin', 'ModelAdmin']


def autodiscover():
    autodiscover_modules('admin')
