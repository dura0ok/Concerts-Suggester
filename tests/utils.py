from functools import wraps


def async_test(f):
    """
    Decorator to create asyncio context for asyncio methods or functions.
    """

    @wraps(f)
    def g(*args, **kwargs):
        args[0].loop.run_until_complete(f(*args, **kwargs))

    return g
