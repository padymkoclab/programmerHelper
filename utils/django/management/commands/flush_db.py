
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.apps import apps


class Command(BaseCommand):

    def handle(self, **kwargs):

        models_with_problems = list()

        for model in apps.get_models():
            qs = model._default_manager.filter()
            try:
                qs.delete()
            except:
                models_with_problems.append(model)
                print('Problems with table "{}"'.format(model._meta.db_table))
            else:
                print('Data from table "{}" successfully deleted'.format(model._meta.db_table))

        if models_with_problems:
            for model in models_with_problems:
                sql_ = "DELETE FROM {}".format(model._meta.db_table)
                model._default_manager.raw(sql_)

        call_command('migrate')
