class Singleton(type):
    """Singleton factory class.

    Creates a singleton object of the inherited class. Inheritnace done via
    metaclass=Singleton in the child class' constructor.
    Any additional keyword args that might be required by the calling class needs to be
    provided via the private method `_get_required_kwargs` implementation.

    Parameters
    ----------
    type: type
        Native type object of Python

    Returns
    -------
    Always returns the same cached instance for the class being called.

    Usage
    -----
    The calling class is turned into a callable like `SingletonClass()`. Calling it
    either creates the instance on the first pass, and thereafter always returns
    the same cached instance.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            get_extra_kwargs = getattr(cls, "_get_required_kwargs", None)

            if callable(get_extra_kwargs):
                extra_kwargs = cls._get_required_kwargs()
            else:
                extra_kwargs = {}

            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **extra_kwargs, **kwargs
            )
        return cls._instances[cls]
