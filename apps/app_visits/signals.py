
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from apps.app_articles.models import Article


@receiver(pre_save, sender=[Article])
def signal_change_slug(sender, instance, **kwargs):
    print('Save')
    # change in model Visit name instance if it is updated
