import math
from decimal import Decimal

from ..trading_signal import TradingSignal
from .singleton_maker import Singleton


class FundsAllocator(metaclass=Singleton):
    def get_permissible_funds(self, trading_signal: TradingSignal) -> Decimal:
        if trading_signal.options_signal:
            allocator = OptionsFundsAllocator()
        else:
            allocator = EquityFundsAllocator()

        return allocator.get_permissible_funds(trading_signal)


class OptionsFundsAllocator(metaclass=Singleton):
    def get_permissible_funds(self, trading_signal: TradingSignal) -> Decimal:
        available_funds = 100
        average_margin_per_lot = 5
        max_lots_possible = math.floor(available_funds / average_margin_per_lot)

        max_trades_to_support = 6

        available_funds_per_trade = math.floor(
            max_lots_possible / max_trades_to_support
        )

        return available_funds_per_trade


class EquityFundsAllocator(metaclass=Singleton):
    def get_permissible_funds(self, trading_signal: TradingSignal) -> Decimal:
        return "ok"
