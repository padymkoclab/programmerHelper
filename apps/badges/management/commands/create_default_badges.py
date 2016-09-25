
import logging
import collections

from django.core.management.base import BaseCommand

from ...constants import BADGES
from ...models import Badge


logger = logging.getLogger('django.development')


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        lst_statuses_created = list()

        for badge in BADGES:

            #
            was_created = Badge.objects.get_or_create(
                name=badge['name'],
                description=badge['description'],
                kind=badge['kind'],
                category=badge['category'],
            )[1]

            lst_statuses_created.append(was_created)

        count_created = collections.Counter(lst_statuses_created)[True]
        count_exists = collections.Counter(lst_statuses_created)[False]

        logger.info('Created {} badges. Already exists {} badges.'.format(count_created, count_exists))
