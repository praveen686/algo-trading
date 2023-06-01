class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        print(f"kwargs={kwargs}, args={args}, cls={cls}")
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
