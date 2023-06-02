import logging

from ..trading_signal import TradingSignal
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

    strategies_manager: object = None
    order_manager: object = None
    funds_manager: object = None

    def place_order_from_call_blob(self, call_blob):
        signal_object = TradingSignal.objects.create_from_call_blob(call_blob)
        return signal_object

    def process_signal(self, trading_signal: TradingSignal):
        return "ok"
