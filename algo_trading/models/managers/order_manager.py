from django.db import models
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

from ..order_history import OrderHistory
from ..trading_signal import TradingSignal


class OrderManager(models.Manager):
    def update_details_and_history(
        self, order_history: list[dict], trading_signal: TradingSignal
    ):
        order = self.create_order_with_first_history(order_history[0], trading_signal)

        for history_item in order_history:
            OrderHistory.objects.create_history_objects_from_broker_data(
                order, history_item
            )

        return order

    def create_order_with_first_history(
        self, order_data: dict, trading_signal: TradingSignal
    ):
        order_data["trading_symbol"] = order_data.pop("tradingsymbol")
        order_data["placed_at"] = make_aware(
            parse_datetime(order_data.pop("order_timestamp"))
        )
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
