from django.db import models
from django.urls import reverse

from .instruments import Instrument
from .trading_signal import TradingSignal


class Order(models.Model):
    trading_symbol = models.CharField("trading symbol", max_length=100, default="")
    exchange = models.CharField("zerdoha exchange", max_length=50, default="")
    order_id = models.BigIntegerField(
        "zerodha order id", default=None, blank=True, null=True
    )
    exchange_order_id = models.BigIntegerField(
        "exchange order id", default=None, blank=True, null=True
    )

    trigger_price = models.DecimalField(
        "order trigger price",
        max_digits=15,
        decimal_places=2,
        default=None,
        blank=True,
        null=True,
    )
    average_entry_price = models.DecimalField(
        "average entry price",
        max_digits=15,
        decimal_places=2,
        default=None,
        blank=True,
        null=True,
    )
    average_closing_price = models.DecimalField(
        "average close price",
        max_digits=15,
        decimal_places=2,
        default=None,
        blank=True,
        null=True,
    )

    quantity = models.IntegerField("quantity", default=0)
    margin_invested = models.DecimalField(
        "margin invested",
        max_digits=15,
        decimal_places=2,
        default=None,
        blank=True,
        null=True,
    )

    placed_at = models.DateTimeField(
        "order placed at", default=None, blank=True, null=True
    )
    executed_at = models.DateTimeField(
        "order executed at", default=None, blank=True, null=True
    )
    closed_at = models.DateTimeField(
        "order closed at", default=None, blank=True, null=True
    )

    p_and_l = models.DecimalField(
        "total P&L", max_digits=15, decimal_places=2, default=0
    )
    p_and_l_percentage = models.DecimalField(
        "P&L percentage", max_digits=15, decimal_places=2, default=0
    )

    closing_duration = models.DateTimeField(
        "close duration", default=None, blank=True, null=True
    )

    status_msg = models.CharField("status msg from broker", max_length=200, default="")

    class OrderTypeChoices(models.TextChoices):
        MARKET = "M", "MARKET"
        LIMIT = "L", "LIMIT"
        STOPLOSS_LIMIT = "SL", "STOPLOSS_LIMIT"
        STOPLOSS_MARKET = "SL-M", "STOPLOSS MARKET"

    class OrderProductTypes(models.TextChoices):
        CNC = "CNC", "Cash and Carry"
        MIS = "MIS", "Margin Intraday Squareoff"
        NRML = "NRML", "NORMAL"

    class OrderTransactionTypeChoices(models.TextChoices):
        BUY = "BUY", "Buy"
        SELL = "SELL", "Sell"

    class OrderStatusChoices(models.TextChoices):
        PUT_ORDER_REQ_RECEIVED = (
            "PUT ORDER REQ RECEIVED",
            "Order request received by broker",
        )
        VALIDATION_PENDING = "VALIDATION PENDING", "Order pending validation by RMS"
        OPEN_PENDING = "OPEN_PENDING", "Order is pending registration at the exchange"
        MODIFY_VALIDATION_PENDING = (
            "MODIFY VALIDATION PENDING",
            "Order's modification values are pending validation by the RMS",
        )
        MODIFY_PENDING = (
            "MODIFY PENDING",
            "Order's modification values are pending registration at the exchange",
        )
        MODIFIED = "MODIFIED", "Order modification successfully applied at exchange"
        TRIGGER_PENDING = (
            "TRIGGER PENDING",
            "Order's placed but the fill is pending based on a trigger price.",
        )
        CANCEL_PENDING = (
            "CANCEL PENDING",
            "Order's cancellation request is pending registration at the exchange",
        )
        AMO_REQ_RECEIVED = (
            "AMO REQ RECEIVED",
            "Same as PUT ORDER REQ RECEIVED, but for AMOs",
        )
        OPEN = "OPEN", "Order still open at exchange"
        CANCELLED = "CANCELLED", "Order cancelled by exchange"
        REJECTED = "REJECTED", "Order rejected by exchange"
        COMPLETE = "COMPLETE", "Order completed at exchange"

    order_type = models.CharField(
        max_length=5,
        choices=OrderTypeChoices.choices,
        default=OrderTypeChoices.LIMIT,
    )

    product_type = models.CharField(
        max_length=5,
        choices=OrderProductTypes.choices,
        default=OrderProductTypes.NRML,
    )

    transaction_type = models.CharField(
        max_length=4,
        choices=OrderTransactionTypeChoices.choices,
        default=OrderTransactionTypeChoices.BUY,
    )

    instrument_type = models.CharField(
        max_length=3,
        choices=Instrument.InstrumentType.choices,
        default=Instrument.InstrumentType.CALL_OPTION,
    )

    status = models.CharField(
        max_length=40,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.PUT_ORDER_REQ_RECEIVED,
    )

    trading_signal = models.OneToOneField(
        TradingSignal,
        on_delete=models.CASCADE,
        related_name="trading_signal",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

        indexes = [
            models.Index(fields=["trading_symbol"], name="order_trading_symbol_idx"),
            models.Index(fields=["trading_signal"], name="order_trading_signal_idx"),
            models.Index(fields=["instrument_type"], name="order_instrument_type_idx"),
            models.Index(fields=["product_type"], name="order_product_type_idx"),
            models.Index(fields=["status"], name="order_status_idx"),
        ]

    def __str__(self):
        return str(self.order_id)

    def get_absolute_url(self):
        return reverse("order", args=[self.id])
