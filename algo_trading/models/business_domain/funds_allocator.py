import math
from decimal import Decimal

from ..trading_signal import TradingSignal
from .kite_broker import KiteBroker
from .singleton_maker import Singleton


class FundsAllocator(metaclass=Singleton):
    kite: KiteBroker = None

    def __init__(self):
        self.kite = KiteBroker()

    def get_permissible_funds(self, trading_signal: TradingSignal) -> Decimal:
        if trading_signal.is_options_signal:
            allocator = OptionsFundsAllocator()
        else:
            allocator = EquityFundsAllocator()

        return allocator.get_permissible_funds(trading_signal)


class OptionsFundsAllocator(metaclass=Singleton):
    def get_permissible_funds(self, trading_signal: TradingSignal) -> Decimal:
        kite = KiteBroker()
        total_available_funds = kite.total_available_funds()["available"]["cash"]

        funds_for_options = self.funds_for_options(total_available_funds)

        # to be calculated from previous trades
        # average_margin_per_lot = 20000.00
        # max_total_options_lots_possible = math.floor(
        #     funds_for_options / average_margin_per_lot
        # )

        # to be calculated based on average closing time for each trade
        max_trades_to_support = 4

        available_funds_per_trade = math.floor(
            funds_for_options / max_trades_to_support
        )

        return available_funds_per_trade

    def funds_for_options(self, total_available_funds: Decimal) -> Decimal:
        """Return funds that can be utilised for Options calls.

        Currently using 80% of capital for options, remaining for Banknifty calls
        @Todo: Formalise this via values from table, that are calculated periodically
        to maximise opportunity! Woah!
        """
        return total_available_funds * 0.8


class EquityFundsAllocator(metaclass=Singleton):
    def get_permissible_funds(self, trading_signal: TradingSignal) -> Decimal:
        return "ok"
