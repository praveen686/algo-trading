from django.db import models
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

from ..order import Order


class OrderHistoryManager(models.Manager):
    def create_history_objects_from_broker_data(self, order: Order, history_item: dict):
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
