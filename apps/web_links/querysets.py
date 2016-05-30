
from django.db import models

from mylabour.utils import get_random_objects


class WebLinkQuerySet(models.QuerySet):
    """

    """

    def random_weblinks(self, count=1):
        """ """

        return get_random_objects(self, count)

    def weblinks_with_count_usage(self):
        """ """

        self.annotate()
