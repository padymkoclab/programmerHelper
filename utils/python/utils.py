"""[summary]

[description]
"""

import io
import base64


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


def run_video_in_jupyter(path):
    """
    path = "/media/wlysenko/66ABF2AC3D03BAAA/Light/Video/Сборка/Пришло время! Пора просыпаться!.mp4"

    """

    from jupyter.core import display

    video = io.open(path, 'r+b').read()
    encoded = base64.b64encode(video)
    display.HTML(data="""
        <video alt="test" controls>
            <source src="data:video/mp4;base64,{0}" type="video/mp4" />
        </video>
        """.format(encoded.decode('ascii')))


def rgb_to_hex(*args):

    if len(args) != 3:
        raise ValueError()

    return '#{0:X}{1:X}{2:X}'.format(*args)


def hex_to_rgb(val):

    val = val.lstrip('#')

    lv = len(val)

    if lv == 3:
        val = ''.join(i * 2 for i in val)
        lv = 6

    return tuple(int(val[i: i + lv // 3], 16) for i in range(0, lv, lv // 3))
