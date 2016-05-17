
from django.db.models.signals import post_save


def ppp(sender, instance, created, raw, using, update_fields, *args, **kwargs):
    object = sender._meta.verbose_name.lower()
    instance = instance.title
    if created:
        action = 'Created'
    else:
        action = 'Updated'
    r = '{action} {object} "{instance}".'.format(action=action, object=object, instance=instance)
    print(r)


post_save.connect(ppp)
