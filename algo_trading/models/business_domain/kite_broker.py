import logging

import environ
from kiteconnect import KiteConnect

from ..instruments import Instrument
from .singleton_maker import Singleton

env = environ.Env()
logger = logging.getLogger(__name__)


class KiteBroker(KiteConnect, metaclass=Singleton):
    EXCHANGES_IN_OPERATION = [
        KiteConnect.EXCHANGE_NSE,
        KiteConnect.EXCHANGE_BSE,
        KiteConnect.EXCHANGE_BFO,
        KiteConnect.EXCHANGE_NFO,
    ]

    def _get_required_kwargs():
        return {"api_key": env("ZERODHA_API_KEY")}

    def set_refresh_token(self, rt):
        self.refresh_token = rt

    def create_session(self, zerodha_request_token):
        return self.generate_session(
            zerodha_request_token, api_secret=env("ZERODHA_API_SECRET")
        )

    def load_instruments_for_today(self):
        logger.info("Starting instruments load")
        instruments_loaded = []

        for exchange in self.EXCHANGES_IN_OPERATION:
            logger.info(f"Starting instruments load for exchange: {exchange}")

            instruments_in_exchange = self.instruments(exchange)
            logger.info(
                f"Found {len(instruments_in_exchange)} instruments in exchange {exchange}"
            )

            newly_created = Instrument.objects.load_bulk_instruments(
                instruments_in_exchange
            )
            logger.info(
                f"Created new {newly_created} instruments for exchange {exchange}"
            )

            instruments_loaded.append({exchange: newly_created})

        return instruments_loaded
