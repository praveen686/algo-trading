from django.db import models

# from ..order_history import OrderHistory


class OrderManager(models.Manager):
    def update_details_and_history(self, order_history: list[dict]):
        first_history = order_history[0]

        order = self.create_order_with_first_history(first_history)
        for history_item in order_history[1:]:
            order.histories.create(history_item)

        return order
