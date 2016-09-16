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


def flatten(sequence):
    """
    Make an iterable, arbitrary-nested object as flatten
    and return it as generator.

    >>> tuple(flatten([[4,5, [2, [3]]], [1,[2, [1, [2]]],3], [1,[2,3]]]))
    (4, 5, 2, 3, 1, 2, 1, 2, 3, 1, 2, 3)
    >>> tuple(flatten([[[[[[[[1, [2, [3, [4, [5, [6, [7, [8, [9]]]]]]]]]]]]]]]]))
    (1, 2, 3, 4, 5, 6, 7, 8, 9)
    >>> tuple(flatten(('aaa', 'ddd', ('bbbb', ('ccc', ('ddd', 'e', 'f'))))))
    ('aaa', 'ddd', 'bbbb', 'ccc', 'ddd', 'e', 'f')
    """

    for i in sequence:
        if isinstance(i, (list, tuple)):
            yield from flatten(i)
        else:
            yield i
