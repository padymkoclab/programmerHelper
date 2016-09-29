

class SiteAdminStrictDescriptor:
    """

    """

    def __init__(self, admin_site):
        self.admin_site = admin_site

    def __get__(self, intance, owner):
        return self.admin_site

    def __set__(self, intance, value):

        from .site import SiteAdmin

        if not isinstance(value, SiteAdmin):
            raise TypeError('Attribute "site_admin" must be instance of {}'.format(SiteAdmin))
        self.admin_site = value

    def __delete__(self, instance):
        del self.admin_site


class ModelAdminStrictDescriptor:
    """

    """

    def __init__(self, admin_model):
        self.admin_model = admin_model

    def __get__(self, intance, owner):
        return self.admin_model

    def __set__(self, intance, value):

        from .admin import ModelAdmin

        if not isinstance(value, ModelAdmin):
            raise TypeError('Attribute "model_admin" must be instance of {}'.format(ModelAdmin))
        self.admin_model = value

    def __delete__(self, instance):
        del self.admin_model
