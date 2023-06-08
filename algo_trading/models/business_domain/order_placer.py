import math
from decimal import Decimal

from ..order import Order
from ..trading_signal import TradingSignal
from .funds_allocator import FundsAllocator
from .kite_broker import KiteBroker
from .singleton_maker import Singleton


class OrderPlacer(metaclass=Singleton):
    """
    The OrderPlacer class handles the placement and processing of orders in a
    trading system.

    Class Variables:
        funds_allocator (FundsAllocator): An instance of the FundsAllocator
            class for managing fund allocation.
        kite (KiteBroker): An instance of the KiteBroker class for interacting
            with the broker.

    Methods:
        --> __init__(): Initializes the OrderPlacer class by creating instances of
            FundsAllocator and KiteBroker.

        --> process_signal(trading_signal: TradingSignal) -> None: Processes a
            trading signal and returns the order ID.

        --> place_options_order_at_broker(trading_signal: TradingSignal) -> int:
            Places an options order at the broker and returns the order ID.

        --> get_ltp_and_margin_per_lot(trading_signal: TradingSignal) -> Decimal:
            Retrieves the Last Traded Price (LTP) and margin per lot.

        --> record_order_details_from_broker(order_id_at_broker: int,
            trading_signal: TradingSignal) -> Order: Records order details
            from the broker and returns the updated Order object.
    """

    funds_allocator: FundsAllocator = None
    kite: KiteBroker = None

    def __init__(self):
        self.funds_allocator = FundsAllocator()
        self.kite = KiteBroker()

    def process_signal(self, trading_signal: TradingSignal) -> None:
        """Process a trading signal and return the order ID.

        Args:
            trading_signal (TradingSignal): The trading signal to be processed.

        Returns:
            None

        Description:
        - Processes the given trading signal.
        - Retrieves the order ID at the broker.
        - Records order details from the broker.
        - Installs order updates.
        - Updates objects with order details.
        - Returns the ID of the order object.
        """

        order_id_at_broker = self.place_options_order_at_broker(trading_signal)
        print(f"------- order_id_at_broker: {order_id_at_broker}")

        order_object = self.record_order_details_from_broker(
            order_id_at_broker, trading_signal
        )
        print(f"------- order_object= {order_object}")

        self.install_order_updates_for(order_object)

        self.update_objects_with_order_details(trading_signal, order_object)

        return order_object.id

    def place_options_order_at_broker(self, trading_signal: TradingSignal) -> int:
        """Place an options order at the broker and return the order ID.

        Args:
            trading_signal (TradingSignal): The trading signal containing information
            for the order placement.

        Returns:
            int: The order ID at the broker.

        Description:
        - Places an options order at the broker based on the given trading signal.
        - Calculates the funds available for trade.
        - Retrieves the margin required per lot and the last known LTP
        - Determines the number of lots to take based on available funds and margin/lot.
        - Returns the order ID at the broker.
        """

        funds_for_trade = self.funds_allocator.get_permissible_funds(trading_signal)

        (margin_required_per_lot, last_known_ltp) = self.get_ltp_and_margin_per_lot(
            trading_signal
        )

        lots_to_take = math.floor(funds_for_trade / margin_required_per_lot)

        return self.kite.place_options_order(
            trading_signal, lots_to_take, last_known_ltp
        )

    def get_ltp_and_margin_per_lot(self, trading_signal: TradingSignal) -> Decimal:
        """Get the Last Traded Price (LTP) and margin per lot.

        Args:
            trading_signal (TradingSignal): The trading signal containing the symbol
            and lot size information.

        Returns:
            Decimal: The margin required per lot.

        Description:
        - Retrieves the Last Traded Price (LTP) and margin required per lot.
        - Obtains the broker symbol for the given trading signal.
        - Retrieves the last known LTP for the broker symbol.
        - Calculates the margin required/lot based on the last known LTP and lot size.
        - Returns the margin required per lot.
        """

        broker_symbol = trading_signal.symbol_for_broker_query()
        last_known_ltp = self.kite.last_known_ltp(broker_symbol)

        return (last_known_ltp * trading_signal.lot_size, last_known_ltp)

    def record_order_details_from_broker(
        self, order_id_at_broker: int, trading_signal: TradingSignal
    ) -> Order:
        """Record order details from the broker and return the updated Order object.

        Args:
            order_id_at_broker (int): The order ID obtained from the broker.
            trading_signal (TradingSignal): trading signal associated with the order.

        Returns:
            Order: The updated Order object.

        Description:
        - Retrieves the order history from the broker using the order ID.
        - Updates the order details and history using
        Order.objects.create_order_and_record_history() method.
        - Returns the updated Order object.
        """

        order_history = self.kite.order_history(order_id_at_broker)["data"]

        order = Order.objects.create_order_and_record_history(
            order_history, trading_signal
        )
        return order

    def install_order_updates_for(self, order_object: Order) -> None:
        return "install kite listeners"

    def update_objects_with_order_details(
        self, trading_signal: TradingSignal, order_object: Order
    ) -> None:
        return "update Tsig status, attach order to Tsig"
