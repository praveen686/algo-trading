from django.db import models
from django.urls import reverse

from .managers import InstrumentManager


class Instrument(models.Model):
    symbol = models.CharField(max_length=20, db_index=True, unique=True)
    descriptive_name = models.CharField(max_length=100)
    first_open_date = models.DateField("instrument first traded date", default=None, null=True, blank=True)

    class InstrumentType(models.TextChoices):
        STOCK = 'ST', 'Stock'
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
       default=InstrumentType.STOCK,
    )

    class Meta:
        verbose_name = "Instrument"
        verbose_name_plural = "Instruments"

    def __str__(self):
        return self.descriptive_name

    # def save(self):
    #     pass

    def get_absolute_url(self):
        return (reverse('instrument-symbol', args=[self.symbol]))

    # TODO: Define custom methods here
    objects = InstrumentManager()
