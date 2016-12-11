
from utils.django.viewmixins import ContextTitleMixin

from .descriptors import SiteAdminStrictDescriptor, ModelAdminStrictDescriptor, SiteAppAdminStrictDescriptor


class SiteAdminMixin(ContextTitleMixin):

    site_admin = SiteAdminStrictDescriptor('site_admin')

    def __init__(self, site_admin, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.site_admin = site_admin


class SiteModelAdminMixin(SiteAdminMixin):

    model_admin = ModelAdminStrictDescriptor('model_admin')

    def __init__(self, model_admin, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.model_admin = model_admin


class SiteAppAdminMixin(SiteAdminMixin):

    app_config = SiteAppAdminStrictDescriptor('app_config')

    def __init__(self, app_config, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.app_config = app_config
