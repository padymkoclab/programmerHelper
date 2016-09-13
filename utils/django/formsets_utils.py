
import collections


def find_dublication_on_formset(formset, field, msg_for_all, msg_for_obj):
    """ """

    if not formset.total_error_count():

        objects = (cleaned_data[field] for cleaned_data in formset.cleaned_data)

        counter_objects = collections.Counter(objects)

        repeated_objects = [item[0] for item in counter_objects.items() if item[1] > 1]

        if repeated_objects:
            formset.non_form_errors().append(msg_for_all)
            for form in formset.forms:
                if form.cleaned_data[field] in repeated_objects:
                    form.add_error(field, msg_for_obj)
