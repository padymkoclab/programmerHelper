"""[summary]

[description]
"""


def check_method_of_object(obj, method):
    """ """

    try:
        attr = getattr(obj, method)
    except AttributeError:
        raise Exception('Object has not method "{}"'.format(method))
    else:
        if not callable(attr):
            raise Exception('Attribute {} of the object is not callable'.format(method))


def split_sequence_to_chunks(sequence, n):
    """ """

    if n < 1:
        raise ValueError()

    chuncks = list()
    for i in range(0, len(sequence), n):
        chuncks.append(sequence[i: i + n])
    return chuncks
