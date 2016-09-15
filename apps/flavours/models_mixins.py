
from django.utils.translation import ugettext_lazy as _


class FlavourModelMixin:

    def get_count_flavours(self):
        """ """

        if hasattr(self, 'count_flavours'):
            return self.count_flavours

        return self.flavours.count()
    get_count_flavours.admin_order_field = 'count_flavours'
    get_count_flavours.short_description = _('Count flavours')

    def get_count_like_flavours(self):
        """ """

        return self.flavours.filter(status=True).count()
    get_count_like_flavours.short_description = _('Count likes flavorites')

    def get_count_dislike_flavours(self):
        """ """

        return self.flavours.filter(status=False).count()
    get_count_dislike_flavours.short_description = _('Count dislike flavorites')
