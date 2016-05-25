
from django import setup
from django.apps import apps

if not apps.ready:
    setup()

from apps.app_tags.factories import factory_tags
from apps.app_web_links.factories import factory_web_links
from apps.app_badges.factories import factory_badges
from apps.app_solutions.factories import factory_categories_of_solutions_and_solutions
from apps.app_accounts.factories import factory_account_level, factory_accounts

factory_tags()
factory_web_links(50)
factory_badges()
factory_account_level()
factory_accounts(15)
# factory_categories_of_solutions_and_solutions(count_solutions=20)
