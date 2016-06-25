
from django.db import models


class ActivityManager(models.Manager):
    """

    """

    def show_last_actions(self, count=10):
        for i in self.all()[:10]:
            print(i)
