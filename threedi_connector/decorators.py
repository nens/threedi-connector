"""Useful decorators."""
from functools import wraps

from .helpers import get_credentials_interactively


def authenticate_interactively(func):
    """
    Require authentication as default, and ask via stdin for username/pw
    if it isn't supplied.

    Notes:

    Authentication can still be disabled by passing ``use_auth=False``.

    To authenticate non-interactively, use the ``auth`` argument, i.e.:
    ``func(auth=Credentials(username='foo', password='bar'))``
    """
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        """
        Wraps a HTTP method function

        This wrapper introduces the following extra kwargs:
            use_auth (bool): enable or disable authentication completely.
                Default: True
        """
        use_auth = kwargs.pop('use_auth', True)
        if use_auth:
            auth = kwargs.get('auth')
            if not auth:
                kwargs['auth'] = get_credentials_interactively()
        return func(*args, **kwargs)
    return func_wrapper


def add_auth_creds_from_self(creds_attribute_name='_AddCredsMixin__creds'):
    """A decorator to parameterize the real decorator
    ``_add_auth_creds_from_self`` to make it more flexible."""
    def _add_auth_creds_from_self(func_requiring_creds):
        """If the API object has been authenticated using the
        ``AddCredsMixin.authenticate`` method, this decorator will pass on
        those credentials as keyword arguments to ``func_requiring_creds``
        using the ``auth`` keyword.

        Requirements:

        - The wrappee ``func_requiring_creds`` needs to be a function that
        accepts ``auth=creds`` as keyword arguments.

        - ``func_requiring_creds`` should be an instance method of an object
        subclassed using ``AddCredsMixin``, since we need to inspect variables
        set by that mixin.
        """
        @wraps(func_requiring_creds)
        def func_wrapper(*args, **kwargs):
            instance = args[0]  # i.e.: self
            creds = getattr(instance, creds_attribute_name)
            if creds is not None:
                assert isinstance(creds, tuple), 'sanity check'
                return func_requiring_creds(auth=creds, *args, **kwargs)
            else:
                return func_requiring_creds(*args, **kwargs)
        return func_wrapper
    return _add_auth_creds_from_self
