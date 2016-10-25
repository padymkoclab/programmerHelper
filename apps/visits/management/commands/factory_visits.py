

import datetime
from unittest import mock
import random
import logging

from django.utils import timezone
from django.contrib.auth import get_user_model

from factory import fuzzy

from utils.django.basecommands import FactoryCountBaseCommand

from ...utils import update_user_pks
from ...models import Visit, Attendance, VisitPage, VisitUserBrowser, VisitUserSystem


logger = logging.getLogger('django.development')


class Command(FactoryCountBaseCommand):

    OS = ('Linux', 'Windows', 'Macintosh')
    BROWSERS = ('Chrome', 'Opera', 'Firefox', 'Edge', 'Internet Explorer')
    URLS = (
        '/',
        '/admin/',
        '/main/',
        '/index/',
        '/articles/',
        '/blog/',
        '/blog/entries/1',
        '/blog/entries/2',
        '/blog/entries/3',
    )

    def add_arguments(self, parser):

        parser.add_argument('count_visits', nargs=1, type=self._positive_integer_from_1_to_999)

    def handle(self, *args, **kwargs):

        count_visits = kwargs.get('count_visits')[0] or 500

        # clear old visits
        Visit._default_manager.filter().delete()
        Attendance._default_manager.filter().delete()
        VisitPage._default_manager.filter().delete()
        VisitUserBrowser._default_manager.filter().delete()
        VisitUserSystem._default_manager.filter().delete()

        users = get_user_model()._default_manager.all()

        for i in range(100, 0, -1):
            attendance = Attendance.objects.create()
            attendance.date = timezone.now().date() - timezone.timedelta(days=i)
            attendance.full_clean()
            attendance.save()

        for i in range(count_visits):

            user = random.choice(users)

            attendance = random.choice(tuple(Attendance.objects.all()))
            attendance.users.add(user)

            url = random.choice(self.URLS)

            fake_request = mock.MagicMock()
            fake_request.path_info = url
            VisitPage.objects.change_url_counter(fake_request)

            browser_name = random.choice(self.BROWSERS)
            update_user_pks(VisitUserBrowser, browser_name, user)

            os_name = random.choice(self.OS)
            update_user_pks(VisitUserSystem, os_name, user)

            start_day = datetime.datetime.fromordinal(attendance.date.toordinal())
            start_day = start_day.replace(tzinfo=timezone.get_current_timezone())

            end_day = start_day.replace(hour=23, minute=59, second=59, microsecond=999999)

            date = fuzzy.FuzzyDateTime(start_day, end_day).fuzz()

            if not Visit._default_manager.filter(user=user).exists():
                visit = Visit._default_manager.create(user=user)
                Visit._default_manager.filter(pk=visit.pk).update(date=date)
            else:
                visit = Visit._default_manager.get(user=user)
                if date > visit.date:
                    Visit._default_manager.filter(pk=visit.pk).update(date=date)

        Attendance._default_manager.filter(users__isnull=True).delete()

        logger.info('Made factory {} visits for {} users on {} days.'.format(
            count_visits,
            Visit._default_manager.count(),
            Attendance._default_manager.count(),
        ))
