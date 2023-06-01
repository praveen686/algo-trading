from django.db import models
from django.urls import reverse

from .instruments import Instrument


class TradingSignal(models.Model):
    created_at = models.DateTimeField("created at")
    fulfilled_at = models.DateTimeField("fulfilled at")
    exited_at = models.DateTimeField("exited at")
    signal_source = models.CharField("source of signal", max_length=100, default="")

    instrument_type = models.CharField(
        max_length=4,
        choices=Instrument.InstrumentType.choices,
        default=Instrument.InstrumentType.EQUITY,
    )

    class TradingSignalType(models.TextChoices):
        BUY = "BUY", "BUY"
        SELL = "SELL", "SELL"

    signal_type = models.CharField(
        max_length=4,
        choices=TradingSignalType.choices,
        default=TradingSignalType.BUY,
    )

    entry_point = models.DecimalField(
        "entry point",
        default=None,
        null=True,
        blank=True,
        max_digits=15,
        decimal_places=5,
    )
    stoploss_point = models.DecimalField(
        "stoploss point",
        default=None,
        null=True,
        blank=True,
        max_digits=15,
        decimal_places=5,
    )
    target1 = models.DecimalField(
        "target 1",
        default=None,
        null=True,
        blank=True,
        max_digits=15,
        decimal_places=5,
    )
    target2 = models.DecimalField(
        "target 2",
        default=None,
        null=True,
        blank=True,
        max_digits=15,
        decimal_places=5,
    )
    # Ununsed for now, but kept for future uses
    target3 = models.DecimalField(
        "target 3",
        default=None,
        null=True,
        blank=True,
        max_digits=15,
        decimal_places=5,
    )
    lot_size = models.IntegerField(
        "lot size",
        default=None,
        null=True,
        blank=True,
    )
    tick_size = models.DecimalField(
        "tick size",
        default=None,
        null=True,
        blank=True,
        max_digits=15,
        decimal_places=5,
    )

    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Trading Signal"
        verbose_name_plural = "Trading Signals"

        indexes = [
            models.Index(fields=["instrument_id"], name="signal_instrument_id"),
            models.Index(
                fields=["signal_type", "instrument_id"],
                name="signal_type_and_instrument",
            ),
        ]

        get_latest_by = "id"

    def __str__(self):
        return f"{self.signal_type}: {self.instrument__name} at {self.entry_point}, SL: {self.stoploss_point}, targets: {self.target1}, {self.target2}"

    def get_absolute_url(self):
        return reverse("trading-signal", args=[self.id])
