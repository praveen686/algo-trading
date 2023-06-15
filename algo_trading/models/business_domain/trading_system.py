import logging

from ..order import Order
from ..trading_signal import TradingSignal
from .order_placer import OrderPlacer
from .signal_manager import SignalManager
from .singleton_maker import Singleton

logger = logging.getLogger(__name__)


class TradingSystem(metaclass=Singleton):
    """Business object that manages the entire trading system

    Responsible for making decisions on trading signals, in accordance with funds
    available.
    Houses settings for system wide thresholds on P&L margins, trade limits and
    other global settings.
    Contains references to `OrderManager` for managing orders
    `FundsManager` for gathering info on funds available overall and per trade position
    `StrategiesManager` for tracking strategies and their performances

    """

    def __init__(self):
        self.order_placer = OrderPlacer()
        self.signal_manager = SignalManager()

    strategies_manager: object = None
    order_placer: OrderPlacer = None
    signal_manager: SignalManager = None

    def place_order_from_call_blob(
        self, call_blob: str
    ) -> tuple([TradingSignal, Order]):
        """
        Places an order based on a call blob and returns the trading signal.

        Args:
            call_blob (CallBlob): The call blob for creating the options signal.

        Returns:
            tuple([TradingSignal, Order]):
                (The generated trading signal, the generated order object)

        Description:
        - Converts the call blob into an options trading_signal.
        - Processes the trading signal using the order placer to create an order
        - Returns the generated trading signal, and the order object
        """
        trading_signal = self.signal_manager.create_options_signal_from_call(call_blob)
        order = self.order_placer.process_signal(trading_signal)

        return (trading_signal, order)
