import datetime
import re

from django.db import models

from ..instruments import Instrument


class TradingSignalManager(models.Manager):
    def create_from_call_blob(self, call_blob):
        print(f"call_blob= {call_blob}, type={type(call_blob)}")
        lines = call_blob.split("\r\n")
        print(f"lines = {lines}")

        instrument_name = lines[0].strip()
        entry_line = lines[1].strip()
        targets_line = lines[2].strip()
        stoploss_line = lines[3].strip()

        entry_point = re.search(r"Entry - (.*)", entry_line)[1].strip()
        stoploss_point = re.search(r"Stoploss - (.*)", stoploss_line)[1].strip()
        targets = re.search(r"Targets - (.*)", targets_line)[1].strip()
        target1, target2 = [x.strip() for x in targets.split(",")]
        target2 = re.search(r"(.*)\+", target2)[1]

        option_type = instrument_name[-2:]

        instrument = Instrument.objects.get_by_symbol(instrument_name)

        signal = self.create(
            signal_type=self.model.TradingSignalType.BUY,
            instrument_type=option_type,
            entry_point=entry_point,
            stoploss_point=stoploss_point,
            target1=target1,
            target2=target2,
            lot_size=instrument.lot_size,
            tick_size=instrument.tick_size,
            instrument=instrument,
            created_at=datetime.datetime.now(),
            signal_source="Praveen Calls",
        )

        return signal
