from django.db import models
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

from ..order import Order


class OrderHistoryManager(models.Manager):
    def create_history_objects_from_broker_data(self, order: Order, history_item: dict):
        """
        Creates history objects from broker data and associates them with given order

        Args:
            order (Order): The order object to associate the history objects with.
            history_item (dict): The dictionary containing broker data for
            a specific history item.

        Returns:
            OrderHistory: The created history object.

        Description:
        - Converts the order timestamp to a timezone-aware datetime object.
        - Defines a list of required fields from the broker data payload.
        - Extracts the required fields from the history item dictionary.
        - Creates an order history object with the extracted payload.
        - Returns the created history object.
        """
        history_item["timestamp"] = make_aware(
            parse_datetime(history_item["order_timestamp"])
        )

        required_fields_from_payload = [
            "timestamp",
            "cancelled_quantity",
            "filled_quantity",
            "pending_quantity",
            "status",
            "status_message",
        ]

        payload = {k: history_item[k] for k in required_fields_from_payload}

        return order.order_history_set.create(**payload)
