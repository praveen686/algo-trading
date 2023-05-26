import environ
import logging
from kiteconnect import KiteConnect
from .instruments import Instrument

env = environ.Env()
logger = logging.getLogger(__name__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, api_key=env('ZERODHA_API_KEY'), **kwargs)
        return cls._instances[cls]


class KiteBroker(KiteConnect, metaclass=Singleton):
    api_key: str = None
    api_secret: str = None

    EXCHANGES_IN_OPERATION = [
        KiteConnect.EXCHANGE_NSE,
        KiteConnect.EXCHANGE_BSE,
        KiteConnect.EXCHANGE_BFO,
        KiteConnect.EXCHANGE_NFO,
    ]

    def set_refresh_token(self, rt):
        self.refresh_token = rt

    def create_session(self, zerodha_request_token):
        return self.generate_session(zerodha_request_token, api_secret=env('ZERODHA_API_SECRET'))

    def load_instruments_for_today(self):
        print("Starting instruments load")
        instruments_loaded = []

        for exchange in self.EXCHANGES_IN_OPERATION:
            print(f"Starting instruments load for exchange: {exchange}")

            instruments_in_exchange = self.instruments(exchange)
            print(f"Found {len(instruments_in_exchange)} instruments in exchange {exchange}")

            newly_created = Instrument.objects.load_bulk_instruments(instruments_in_exchange)

            instruments_loaded.append({exchange: newly_created})

        return instruments_loaded
