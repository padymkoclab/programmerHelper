

def check_boolean_return(func, *agrs, **kwargs):

    def _wrap(*agrs, **kwargs):

        result = func(*agrs, **kwargs)

        if not isinstance(result, bool):
            raise ValueError('Checker must be return boolean')

        return result

    return _wrap
