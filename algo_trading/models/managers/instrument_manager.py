import datetime

from django.db import models
import yfinance as yf

from ...exceptions import InvalidTickerSymbolError


class InstrumentManager(models.Manager):
    KEY_FOR_SYMBOL_IN_INFO = 'symbol'
    KEY_FOR_DESCRIPTIVE_NAME_IN_INFO = 'longName'
    KEY_FOR_FIRST_OPEN_DATE_IN_INFO = 'firstTradeDateMilliseconds'
    KEY_FOR_INSTRUMENT_TYPE_IN_INFO = 'typeDisp'

    def process_new_instrument(self, new_symbol):
        """ Grab OHLCV data for the given symbol for all time
            Create an Instrument Record for the symbol
            Create OHLCV records for all obtained data
            Raise error if API fails or incorrect symbol is used
        """
        try:
            ticker = yf.Ticker(new_symbol)
            instrument_info = ticker.info

            return self.ingest_new_instrument(instrument_info)
        except AttributeError as error:
            if 'NoneType' in error.args[0]:
                raise InvalidTickerSymbolError
            else:
                raise error
        except Exception as exc:
            raise exc

    def ingest_new_instrument(self, info):
        """ Grab info and create an instrument out of that"""
        first_open_date_from_info = info[self.KEY_FOR_FIRST_OPEN_DATE_IN_INFO] / 1000
        first_open_date = datetime.datetime.fromtimestamp(first_open_date_from_info)

        instrument_type_from_info = info[self.KEY_FOR_INSTRUMENT_TYPE_IN_INFO]
        instrument_type = {i.label: i.value for i in self.model.InstrumentType}[instrument_type_from_info] # noqa

        return self.create(
            symbol=info[self.KEY_FOR_SYMBOL_IN_INFO],
            descriptive_name=info[self.KEY_FOR_DESCRIPTIVE_NAME_IN_INFO],
            first_open_date=first_open_date,
            instrument_type=instrument_type,
        )

    def download_historical_data(self, instruments):
        """Download historical data for all the instruments passed"""
