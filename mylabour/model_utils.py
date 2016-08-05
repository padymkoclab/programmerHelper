
import random

from django.db import models

from .utils import create_logger_by_filename


logger = create_logger_by_filename(__name__)


def get_random_objects(queryset, count, single_as_qs=False):
    """Return certain count random objects from queryset.
    If 'count' is great than queryset, then return all avaibled objects.
    If queryset is empty - raise error."""

    #
    if count < 1:
        return queryset.none()

    #
    if not queryset.count():
        raise queryset.model.DoesNotExist('Passed queryset is empty.')

    #
    if queryset.count() == 1:
        logger.warn('In queryset only 1 object, thus returned it.')
        if single_as_qs:
            return queryset.filter()
        return queryset.first()

    #
    all_primary_keys = list(queryset.values_list('pk', flat=True))
    if len(all_primary_keys) < count:
        raise ValueError('Deficiently objects for choice.')

    #
    random.shuffle(all_primary_keys)
    choiced_primary_keys = all_primary_keys[:count]
    random_objects = queryset.filter(pk__in=choiced_primary_keys)

    #
    if count == 1:
        if single_as_qs:
            return queryset.filter()
        return random_objects.first()

    # prevent dublicates through SQL
    random_objects = random_objects.distinct()

    return random_objects


def leave_only_predetermined_number_of_objects(model, count):
    """Leave only, in place, a predetermined amout objects in a passed model.
    If count objects is less than or equal passed count, leaving the model without changes."""

    # validation input

    # if model is not django`s model
    if not issubclass(model, models.Model):
        msg = 'Parameter \'model\' must be a subclass of the models.Model, but not {0}'.format(type(model))
        raise TypeError(msg)

    # if count is not integer
    if not isinstance(count, int):
        msg = 'Parameter \'count\' must be integer, but not {0}.'.format(type(count))
        raise TypeError(msg)

    # if count is less zero, no sense to continue
    if count < 0:
        return

    # if need to remove all objects
    if count == 0:
        model.objects.filter().delete()

    # get count objects in the model
    count_objects = model.objects.count()

    # if the model has less objects than the passed count,
    # must no changes occur with the model
    if count >= count_objects:
        logger.debug('A count objects is less or equal the passed count. The model was not changed.')
        return

    # a number of objects for removal
    count_objects_for_removal = count_objects - count

    # get objects for removal
    objects_for_removal = get_random_objects(model.objects, count_objects_for_removal)

    # if it is single object, make removal directly
    if isinstance(objects_for_removal, model):
        objects_for_removal.delete()

    # if is a queryset of objects
    else:

        # get primary keys of the objects for removal
        pks_objects_for_removal = objects_for_removal.values('pk')

        # make filter the objects for removal and to remove it
        model.objects.filter(pk__in=pks_objects_for_removal).delete()
