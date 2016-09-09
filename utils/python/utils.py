"""[summary]

[description]
"""


def check_method_of_object(obj, method):
    """ """

    try:
        attr = getattr(obj, method)
    except AttributeError:
        raise Exception('Objet has not method "{}"'.format(method))
    else:
        if not callable(attr):
            raise Exception('Attribute {} of the object is not callable'.format(method))
