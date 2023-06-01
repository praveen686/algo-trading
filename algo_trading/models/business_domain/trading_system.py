import logging

from ..trading_signal import TradingSignal
from .singleton_maker import Singleton

logger = logging.getLogger(__name__)


class TradingSystem(metaclass=Singleton):
    strategies_manager: object = None
    order_manager: object = None
    funds_manager: object = None

    def place_order_from_call_blob(self, call_blob):
        signal_attrs = self.gather_signal_details_from_options_call(call_blob)
        signal_object = self.create_signal(signal_attrs)
        order_object = self.process_signal(signal_object)
        return order_object

    def gather_signal_details_from_options_call(self, call_blob: dict):
        return "ok"

    def create_signal(self, signal_attrs: dict) -> TradingSignal:
        return "ok"

    def process_signal(self, trading_signal: TradingSignal):
        return "ok"
