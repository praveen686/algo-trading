import math
from decimal import Decimal

from ..trading_signal import TradingSignal
from .funds_allocator import FundsAllocator
from .kite_broker import KiteBroker
from .singleton_maker import Singleton


class OrderPlacer(metaclass=Singleton):
    def process_signal(self, trading_signal: TradingSignal) -> None:
        """process

        gets called from TradingSystem -> OrderPlacer.process_signal(trading_signal)
        """

        kite = KiteBroker()

        order_details = self.place_options_order(trading_signal, kite)

        order_object = self.record_order_at_broker(order_details)

        self.install_order_updates_for(order_object)

        self.update_objects_with_order_details(trading_signal, order_object)

        return order_object.id

    def place_options_order(
        self, trading_signal: TradingSignal, kite: KiteBroker
    ) -> None:
        funds_for_trade = self.get_available_funds()
        margin_required_per_lot = self.get_margin_required_per_lot()

        lots_to_take = math.floor(funds_for_trade / margin_required_per_lot)
        return kite.place_options_order(trading_signal, lots_to_take)

    def get_available_funds(self, trading_signal: TradingSignal) -> Decimal:
        funds_allocator = FundsAllocator()
        return funds_allocator.get_permissible_funds(trading_signal)

    def get_margin_required_per_lot(
        self, trading_signal: TradingSignal, kite: KiteBroker
    ) -> Decimal:
        ltp = kite.ltp(trading_signal)

        return ltp * trading_signal.lot_size

    def record_order_at_broker(self, order_details: dict) -> object:
        return "Model Object.instance created with order_details"

    def install_order_updates_for(self, order_object: object) -> None:
        return "install kite listeners"

    def update_objects_with_order_details(
        self, trading_signal: TradingSignal, order_object: object
    ) -> None:
        return "update Tsig status, attach order to Tsig"
