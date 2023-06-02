from .singleton_maker import Singleton


class OrderCloser(metaclass=Singleton):
    def meth(self):
        return "ok"
