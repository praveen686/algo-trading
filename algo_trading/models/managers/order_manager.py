from django.db import models
from django.utils.timezone import make_aware

from ..trading_signal import TradingSignal


class OrderManager(models.Manager):
    def create_order_and_record_history(
        self, order_history: list[dict], trading_signal: TradingSignal
    ):
        """
        Creates order and creates history items for the given order history.

        Args:
            order_history (list[dict]): The list of order history items.
            trading_signal (TradingSignal): The trading signal associated with the order

        Returns:
            Order: The updated order.

        Description:
        - Creates an order with the first history entry item sufficing all required
        fields for the order. Some fields are still empty, as they've not been filled
        at the exchange at the time of the first order creation steps.
        - Iterates through each history item in the order history, and creates a
        HistoryItem for each update of the order
        - Returns the created & updated order.

        Note:
        - This method assumes that the order history list is ordered chronologically.
        """
        order = self.create_order_with_first_history_item(
            order_history[0], trading_signal
        )

        for history_item in order_history:
            payload = self.get_history_fields_from_broker_data(history_item)

            order.order_history.create(**payload)

        return order

    def create_order_with_first_history_item(
        self, order_data: dict, trading_signal: TradingSignal
    ):
        """
        Creates an order with the first history entry and returns the created order.

        Args:
            order_data (dict): The dictionary containing order data.
            trading_signal (TradingSignal): The trading signal associated with the order

        Returns:
            Order: The created order.

        Description:
        - Renames the 'tradingsymbol' key to 'trading_symbol' in the order data.
        - Converts the 'order_timestamp' to a timezone-aware datetime object.
        - Renames the 'product' key to 'product_type' in the order data.
        - Sets the 'trading_signal' key to the provided trading signal.
        - Defines a list of required fields from the order data payload.
        - Extracts the required fields from the order data to create the order payload.
        - Creates an order with the extracted order payload using the `create` method.
        - Returns the created order.
        """

        order_data["trading_symbol"] = order_data.pop("tradingsymbol")
        order_data["placed_at"] = make_aware(order_data["order_timestamp"])
        order_data["product_type"] = order_data.pop("product")
        order_data["trading_signal"] = trading_signal

        required_fields_from_payload = [
            "exchange",
            "exchange_order_id",
            "placed_at",
            "order_id",
            "order_type",
            "product_type",
            "quantity",
            "status",
            "trading_signal",
            "trading_symbol",
            "transaction_type",
            "trigger_price",
        ]

        order_payload = {k: order_data[k] for k in required_fields_from_payload}

        order = self.create(**order_payload)

        return order

    def get_history_fields_from_broker_data(self, history_item):
        history_item["timestamp"] = make_aware(history_item["order_timestamp"])

        required_fields_from_payload = [
            "timestamp",
            "cancelled_quantity",
            "filled_quantity",
            "pending_quantity",
            "status",
            "status_message",
        ]

        payload = {k: history_item[k] for k in required_fields_from_payload}

        return payload
