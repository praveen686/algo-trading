import environ
from kiteconnect import KiteConnect

env = environ.Env()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, api_key=env('ZERODHA_API_KEY'), **kwargs)
        return cls._instances[cls]


class KiteBroker(KiteConnect, metaclass=Singleton):
    api_key: str = None
    api_secret: str = None

    def set_refresh_token(self, rt):
        self.refresh_token = rt

    def create_session(self, zerodha_request_token):
        return self.generate_session(zerodha_request_token, api_secret=env('ZERODHA_API_SECRET'))
