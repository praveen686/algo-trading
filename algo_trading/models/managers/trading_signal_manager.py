from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet

from ..instruments import Instrument


class TradingSignalManager(models.Manager):
    """Manager class for `TradingSignal`

    Class level functionalities for trading signal go here
    """

    def get_options_calls(self) -> QuerySet:
        """Return all options calls"""

        return (
            super()
            .get_queryset()
            .filter(
                Q(instrument_type=Instrument.InstrumentType.CALL_OPTION)
                | Q(instrument_type=Instrument.InstrumentType.PUT_OPTION)
            )
        )
