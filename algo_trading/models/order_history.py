from django.db import models

from .order import Order


class OrderHistory(models.Model):
    timestamp = models.DateTimeField(
        "status change time", default=None, null=True, blank=True
    )
    cancelled_quantity = models.IntegerField(
        "cancelled quantity", default=None, null=True, blank=True
    )
    filled_quantity = models.IntegerField(
        "filled quantity", default=None, null=True, blank=True
    )
    pending_quantity = models.IntegerField(
        "pending quantity", default=None, null=True, blank=True
    )
    status = models.CharField(
        max_length=40,
        choices=Order.OrderStatusChoices.choices,
        default=None,
        null=True,
        blank=True,
    )
    status_message = models.CharField("status change message", max_length=200)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Order History"
        verbose_name_plural = "Order Histories"

        indexes = [
            models.Index(fields=["status"], name="order_history_status_idx"),
            models.Index(fields=["order"], name="order_history_order_idx"),
        ]

    def __str__(self):
        return f"Status changed to {self.status} at {self.timestamp}"
