
import logging

from django.core.management.base import BaseCommand

from ...constants import Badges
from ...models import Badge


logger = logging.getLogger('django.development')


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        count_created = 0
        count_updated = 0

        # import ipdb; ipdb.set_trace()
        for badge_data in Badges._DEFAULT_BADGES:

            obj, was_created = Badge.objects.update_or_create(
                name=badge_data['name'],
                kind=badge_data['kind'],
                defaults=dict(
                    description=badge_data['description'],
                    category=badge_data['category'],
                ),
            )

            if was_created:
                count_created += 1
                action = 'was created'
            else:
                count_updated += 1
                action = 'was updated'

            print('{} {}.'.format(obj, action))

        logger.info('Were created {} badges. Were updated {} badges.'.format(count_created, count_updated))
