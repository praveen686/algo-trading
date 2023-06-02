from .singleton_maker import Singleton


class OrderPosthumousTracker(metaclass=Singleton):
    def meth(self):
        return "ok"
