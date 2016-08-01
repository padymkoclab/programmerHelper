
import random

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


def leave_only_single_object(model):
    """ """

    first_obj = model.objects.first()
    model.objects.exclude(pk=first_obj.pk).delete()
