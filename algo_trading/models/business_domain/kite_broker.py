import logging
from decimal import Decimal

import environ
from kiteconnect import KiteConnect

from ..instruments import Instrument
from ..trading_signal import TradingSignal
from .singleton_maker import Singleton

env = environ.Env()
logger = logging.getLogger(__name__)


class KiteBroker(KiteConnect, metaclass=Singleton):
    """Wrapper class around `KiteConnect`, making it a singleton/global object.

    Creates a singleton class that serves as the stand-alone broker object and
    houses all operations with the broker.
    """

    EXCHANGES_IN_OPERATION = [
        KiteConnect.EXCHANGE_NSE,
        KiteConnect.EXCHANGE_BSE,
        KiteConnect.EXCHANGE_BFO,
        KiteConnect.EXCHANGE_NFO,
    ]

    def _get_required_kwargs() -> dict:
        """Generate keyword args required by `KiteBroker` to function

        Creates the api_key arg which is required by `KiteConnect` on __init__
        Private method.

        Returns
        -------
        dict:
            Key value pair of the api key for Zerodha
        """

        return {"api_key": env("ZERODHA_API_KEY")}

    def set_refresh_token(self, rt):
        self.refresh_token = rt

    def create_session(self, zerodha_request_token: str):
        """Create access token from the request token for setting the session

        Calls the `generate_session` method on `KiteConnect` with the received
        request token, and the api secret, gets back the access token and returns
        it back

        Parameters
        ----------
        zerodha_request_token: str
            The request token received from Zerodha login

        Returns
        -------
        access_token: str
            Access token from Zerodha indicating an authenticated session
        """

        return self.generate_session(
            zerodha_request_token, api_secret=env("ZERODHA_API_SECRET")
        )

    def load_instruments_for_today(self) -> dict:
        """Common method to load today's instruments available for trade

        Called from the UI as needed, but primarily called from a cron service
        everyday at 8:30 am IST. Fetches the complete list of instruments with
        all their details from Zerodha, and loads them into DB.

        Returns
        -------
        dict:
            Key value pair for each exchange that we operate with.
            Key is the exchange name. Value is the count of the instruments
            that were loaded today/on this run. Older/existing instruments are
            skipped over.

        """

        logger.info("Starting instruments load")
        instruments_loaded = []

        for exchange in self.EXCHANGES_IN_OPERATION:
            logger.info(f"Starting instruments load for exchange: {exchange}")

            instruments_in_exchange = self.instruments(exchange)
            logger.info(
                f"Found {len(instruments_in_exchange)} instruments in exchange {exchange}"  # noqa
            )

            newly_created = Instrument.objects.load_bulk_instruments(
                instruments_in_exchange
            )
            logger.info(
                f"Created new {newly_created} instruments for exchange {exchange}"
            )

            instruments_loaded.append({exchange: newly_created})

        return instruments_loaded

    def total_available_funds(self) -> Decimal:
        return self.margins(segment=KiteConnect.MARGIN_EQUITY)

    def place_options_order(
        self, trading_signal: TradingSignal, lots_to_take: int, last_known_ltp: Decimal
    ) -> int:
        """Place order at broker

        Returns the order_id of the order created at Zerodha.
        The order is not guaranteed to have been executed, need further checks
        """
        return self.place_order(
            variety=KiteConnect.VARIETY_REGULAR,
            exchange=trading_signal.instrument.exchange,
            tradingsymbol=trading_signal.instrument.trading_symbol,
            transaction_type=KiteConnect.TRANSACTION_TYPE_BUY,
            quantity=lots_to_take,
            product=KiteConnect.PRODUCT_NRML,
            order_type=KiteConnect.ORDER_TYPE_LIMIT,
            price=last_known_ltp,
        )

    def last_known_ltp(self, broker_symbol: str) -> Decimal:
        response = self.ltp([broker_symbol])

        return response[broker_symbol]["last_price"]
