from django.db import models
from django.urls import reverse

from .managers import InstrumentManager


class Instrument(models.Model):
    symbol = models.CharField(max_length=20, db_index=True, unique=True)
    descriptive_name = models.CharField(max_length=100)
    first_open_date = models.DateField("instrument first traded date", default=None, null=True, blank=True)

    class InstrumentType(models.TextChoices):
        EQUITY = 'EQ', 'Equity'
        FUTURES = 'FT', 'Futures'
        OPTIONS = 'OT', 'Options'
        INDEX = 'IX', 'Index'
        CURRENCY = 'CU', 'Currency'
        CURRENCY_FUTURES = 'CF', 'Currency Futures'
        CURRENCY_OPTIONS = 'CO', 'Currency Options'
        INDEX_FUTURES = 'IF', 'Index Futures'
        INDEX_OPTIONS = 'IO', 'Index Options'

    instrument_type = models.CharField(
       max_length=2,
       choices=InstrumentType.choices,
       default=InstrumentType.EQUITY,
    )

    # fields to store Zerodha-specific info. All fields are defaulted to empty string since
    # we won't know these until these are queried from Zerodha.
    # @TODO:
    #   Remove this default and make non-nullable once instrument is ingested fully from Zerodha
    zerodha_instrument_token = models.IntegerField("zerodha instrument token", default=0)
    zerodha_exchange_token = models.CharField("zerodha exchange token", max_length=50, default='')
    zerodha_lot_size = models.IntegerField("zerodha lot size", default=0)
    zerodha_segment = models.CharField("zerodha segment", max_length=50, default='')
    zerodha_exchange = models.CharField("zerdoha exchange", max_length=50, default='')
    zerodha_trading_symbol = models.CharField("zerodha trading symbol", max_length=50, default='')

    class Meta:
        verbose_name = "Instrument"
        verbose_name_plural = "Instruments"

        indexes = [
            models.Index(fields=['symbol'], name="instrument_symbol_idx"),
            models.Index(fields=['instrument_type'], name="instrument_instrument_type_idx"),
        ]

        get_latest_by = "id"

    def __str__(self):
        return self.descriptive_name

    def get_absolute_url(self):
        return (reverse('instrument-symbol', args=[self.symbol]))

    # TODO: Define custom methods here
    objects = InstrumentManager()
