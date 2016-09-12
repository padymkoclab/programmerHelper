
import itertools
import random

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.shortcuts import _get_queryset
from django.db import models

from dateutil.relativedelta import relativedelta

from ..python.logging_utils import create_logger_by_filename


logger = create_logger_by_filename(__name__)


def get_admin_url(obj):
    """ """

    return reverse(
        'admin:{0}_{1}_change'.format(obj._meta.app_label, obj._meta.model_name),
        args=(obj.pk,)
    )


def get_statistics_count_objects_for_the_past_year(queryset, date_field_name):
    """ """

    now = timezone.now()

    # get datetime on eleven months ago
    # owing to a number of month will be unique
    eleven_months_ago = now - relativedelta(months=11)

    # set in first day of month
    eleven_months_ago = eleven_months_ago.replace(day=1)

    # filter votes for a last 11 months and current month
    filter_lookup = '%s__gte' % date_field_name
    conditions_filter = {filter_lookup: eleven_months_ago}
    votes = queryset.filter(**conditions_filter)

    number_current_month = now.month
    number_current_year = now.year

    numbers_all_months = list(range(1, 13))

    # make reorder for order all numbers of months
    # where a number of current month is last, whereas a following month is first
    numbers_all_months = numbers_all_months[number_current_month:] + numbers_all_months[:number_current_month]

    #
    result = list()
    for number_month in numbers_all_months:

        # if is number month is more than current, that in month of past year
        year = number_current_year
        if number_month > number_current_month:
            year = number_current_year - 1

        # get abbr local name of month and year
        date_label = now.replace(year=year, month=number_month, day=1).strftime('%b %Y')

        # filter objects for that number of month
        filter_lookup = '%s__month' % date_field_name
        conditions_filter = {filter_lookup: number_month}
        count_obj_in_that_month = votes.filter(**conditions_filter).count()

        #
        result.append((date_label, count_obj_in_that_month))

    return result


def delete_or_create(model, field, value):

    raise NotImplementedError


def get_latest_or_none(model):
    """ """

    qs = _get_queryset(model)

    try:
        return qs.latest()
    except model.DoesNotExist:
        return


def get_random_objects(queryset, count, single_as_qs=False):
    """Return certain count random objects from queryset.
    If 'count' is great than queryset, then return all avaibled objects.
    If queryset query_stringis empty - raise error."""

    #
    if count < 1:
        return queryset.none()

    #
    if not queryset.count():
        raise queryset.model.DoesNotExist('Passed queryset is empty.')

    #
    if queryset.count() == 1:
        logger.warn('In queryset only 1 object, thus returned it.')
        obj = queryset.first()
        if single_as_qs:
            return queryset.filter(pk=obj.pk)
        return obj

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
        obj = random_objects.first()
        if single_as_qs:
            return queryset.filter(pk=obj.pk)
        return obj

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


def get_string_primary_keys_separated_commas(queryset):
    """Return a string of primary keys of objects, passed in a queryset, separated commas."""

    #
    # if queryset created with .prefetch_related(),
    # then it not working with values_list('[field_name]', flat=True), at least in Django 1.9
    # ticket: https://code.djangoproject.com/ticket/26264
    #
    # for some reason does not working catch TypeError for this problem
    #
    # remains the last, make handle getting list of primary keys
    #

    # a two-nested list primary keys
    list_pks = queryset.values_list('pk')

    # a flatten the two-nested list primary keys
    list_pks = itertools.chain.from_iterable(list_pks)

    # convert the primary keys to string. Important for a UUID field.
    list_pks = map(str, list_pks)

    # return a string of the primary keys, separated commas
    return ','.join(list_pks)
