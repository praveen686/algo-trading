from django.db import models
from django.urls import reverse
from django.db.models import Q

from .managers.instrument_manager import InstrumentManager


class Instrument(models.Model):
    symbol = models.CharField(max_length=30, db_index=True, unique=True)

    class InstrumentType(models.TextChoices):
        EQUITY = 'EQ', 'Equity'
        FUTURES = 'FUT', 'Futures'
        CALL_OPTION = 'CE', 'Call Option'
        PUT_OPTION = 'PE', 'Put Option'
        INDEX = 'IX', 'Index'
        CURRENCY = 'CU', 'Currency'
        CURRENCY_FUTURES = 'CF', 'Currency Futures'
        CURRENCY_OPTIONS = 'CO', 'Currency Options'
        INDEX_FUTURES = 'IF', 'Index Futures'
        INDEX_OPTIONS = 'IO', 'Index Options'

    instrument_type = models.CharField(
       max_length=3,
       choices=InstrumentType.choices,
       default=InstrumentType.EQUITY,
    )

    # fields to store Zerodha-specific info.
    instrument_token = models.IntegerField("zerodha instrument token", default=0)
    exchange_token = models.CharField("zerodha exchange token", max_length=100, default='')
    trading_symbol = models.CharField("zerodha trading symbol", max_length=100, default='')
    name = models.CharField("zerodha company name", default=None, null=True, blank=True, max_length=100)
    expiry = models.CharField("zerodha expiry date", default=None, null=True, blank=True, max_length=100)
    strike = models.DecimalField(
        "zerodha strike price",
        default=None,
        null=True,
        blank=True,
        max_digits=15,
        decimal_places=5,
    )
    tick_size = models.DecimalField(
        "zerodha tick size",
        default=None,
        null=True,
        blank=True,
        max_digits=15,
        decimal_places=5,
    )
    lot_size = models.IntegerField("zerodha lot size", default=None, null=True, blank=True)
    segment = models.CharField("zerodha segment", max_length=50, default='')
    exchange = models.CharField("zerdoha exchange", max_length=50, default='')

    class Meta:
        verbose_name = "Instrument"
        verbose_name_plural = "Instruments"

        indexes = [
            models.Index(fields=['symbol'], name="instrument_symbol_idx"),
            models.Index(fields=['instrument_type'], name="instrument_instrument_type_idx"),
            models.Index(fields=['trading_symbol', 'exchange'], name="instrument_identifier_idx"),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=['trading_symbol', 'exchange'],
                name="unique_instrument_identifier",
                condition=~Q(trading_symbol='') & ~Q(exchange=''),
                violation_error_message="Instrument name at exchange already exists",
            )
        ]

        get_latest_by = "id"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return (reverse('instrument-symbol', args=[self.trading_symbol]))

    # TODO: Define custom methods here
    objects = InstrumentManager()
