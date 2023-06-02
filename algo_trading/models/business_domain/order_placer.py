from .singleton_maker import Singleton


class OrderPlacer(metaclass=Singleton):
    def meth(self):
        return "ok"
