from django.db import models
from . import Instrument


class OhlcvDataDaily(models.Model):
    date = models.DateTimeField("trade time")
    open = models.DecimalField("open price", max_digits=15, decimal_places=5)
    high = models.DecimalField("high price", max_digits=15, decimal_places=5)
    low = models.DecimalField("low price", max_digits=15, decimal_places=5)
    close = models.DecimalField("close price", max_digits=15, decimal_places=5)
    volume = models.IntegerField("trade volume")
    dividends = models.DecimalField(
        "dividends",
        max_digits=8,
        decimal_places=2,
        default=0.0,
        null=True,
        blank=True,
    )
    splits = models.DecimalField(
        "splits",
        max_digits=8,
        decimal_places=2,
        default=0.0,
        null=True,
        blank=True,
    )

    # Refers to the instrument to which this daily data set belongs to.
    # Names the objects on `instrument` as daily_data, resulting in the following methods:
    # instrument.daily_data.count(), instrument.daily_data.filter()
    # instrument.daily_data.add()
    # instrument.daily_data.create()
    # instrument.daily_data.remove()
    # instrument.daily_data.clear()
    # instrument.daily_data.set()
    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.CASCADE,
        related_name="daily_data",
    )

    class Meta:
        verbose_name = "OhlcvDataDaily"
        verbose_name_plural = "OhlcvDataDailies"

        indexes = [
            models.Index(fields=['date'], name="ohlcv_daily_date_idx"),
            models.Index(fields=['instrument', 'date'], name="ohlcv_dly_instrument_date_idx"),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=['instrument', 'date'],
                name="unique_instrument_ohlcv_data_daily_date",
                violation_error_message="Date for instrument already exists, must be unique",
            )
        ]

        get_latest_by = "date"  # should it be -date?, check when we have data

        # Adds instrument.get_ohlcv_data_daily_order(), instrument.set_ohlcv_data_daily_order()
        # to Instrument class' instances.
        # Adds ohlcv_data_daily.get_next_in_order(), ohlcv_data_daily.get_previous_in_order() to
        # this class' instances.
        # This implicitly sets the `ordering` field. Don't use ordering again in this model
        order_with_respect_to = "instrument"

    def __str__(self):
        self.date

    def get_absolute_url(self):
        return ('')

    # TODO: Define custom methods here
