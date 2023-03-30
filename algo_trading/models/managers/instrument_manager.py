from django.db import models
import yfinance as yf


class InstrumentManager(models.Manager):
    def process_new_instrument(self, new_symbol):
        ''' Grab OHLCV data for the given symbol for all time
            Create an Instrument Record for the symbol
            Create OHLCV records for all obtained data
            Raise error if API fails or incorrect symbol is used
        '''
        try:
            symbol_ohlc_data = yf.download(new_symbol)
            new_instrument = Instrument.objects.create(
                symbol=new_symbol,
                descriptive_name=symbol_ohlc_data,
                first_open_date=symbol_ohlc_data,
                instrument_type=symbol_ohlc_data,
            )
        except ImportError:
            return "error"
