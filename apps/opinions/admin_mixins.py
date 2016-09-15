
from django.utils.translation import ugettext_lazy as _

from utils.django.admin_utils import listing_objects_with_admin_url


class OpinionsAdminMixin:

    def get_listing_critics_with_admin_urls(self, obj):
        """ """

        return listing_objects_with_admin_url(
            obj.get_critics(),
            'get_admin_url',
            'get_full_name',
            _('No body')
        )
    get_listing_critics_with_admin_urls.short_description = _('Critics')

    def get_listing_supporters_with_admin_urls(self, obj):
        """ """

        return listing_objects_with_admin_url(
            obj.get_supporters(),
            'get_admin_url',
            'get_full_name',
            _('No body')
        )
    get_listing_supporters_with_admin_urls.short_description = _('Supporters')
