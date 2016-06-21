
import warnings
import urllib

from django.db import models

from mylabour.utils import get_random_objects, has_connect_to_internet


class WebLinkQuerySet(models.QuerySet):
    """
    Queyrset for weblinks to another objects.
    """

    def random_weblinks(self, count=1):
        """Return determined count random weblinks as queryset, if count not equal 1, otherwise return single object."""

        return get_random_objects(self, count)

    def weblinks_with_status(self):
        """Determined status each web link active or broken. If not connect to internet return weblinks with vague status."""

        # check up connect to internet
        if not has_connect_to_internet():
            warnings.warn('Problem this connect to internet.', Warning)
            return self.annotate(is_active=models.Case(
                models.When(pk__isnull=True, then=False),
                default=None,
                output_field=models.BooleanField(),
            ))

        # found and filter broken weblinks
        pks_broken_weblinks = list()
        for weblink in self.iterator():
            try:
                urllib.request.urlopen(weblink.url)
            except:
                pks_broken_weblinks.append(weblink.pk)
        return self.annotate(is_active=models.Case(
            models.When(pk__in=pks_broken_weblinks, then=False),
            default=True,
            output_field=models.BooleanField(),
        ))

    def broken_weblinks(self):
        """Filter weblink with broken URL, if have connect to internet, otherwise return nothing."""

        self = self.weblinks_with_status()
        return self.filter(is_active=False)

    def weblinks_from_youtube(self):
        """Weblinks leading to youtube.com."""

        return self.filter(url__icontains='www.youtube.com')
