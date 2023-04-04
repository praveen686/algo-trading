import datetime

from django.db import models
import yfinance as yf
import pandas as pd

from ...exceptions import InvalidTickerSymbolError


class InstrumentManager(models.Manager):
    KEY_FOR_SYMBOL_IN_INFO = 'symbol'
    KEY_FOR_DESCRIPTIVE_NAME_IN_INFO = 'longName'
    KEY_FOR_FIRST_OPEN_DATE_IN_INFO = 'firstTradeDateMilliseconds'
    KEY_FOR_INSTRUMENT_TYPE_IN_INFO = 'typeDisp'

    def process_new_instrument(self, new_symbol: str):
        """Process a new symbol to be recorded in the model `Instrument`

        Verify if the symbol is a valid one, if not raise an error
        Gather `info` for the symbol from the yfinance API
        Ingest that info into a new record
        Raise error if API fails

        Parameters
        ----------
        new_symbol: str
            The symbol of the instrument that needs to be processed

        Returns
        -------
        The new `Instrument` instance that is created for the symbol.

        Raises
        ------
        InvalidTickerSymbolError
            If the symbol was invalid and no data can be found in yfinance
        AttributeError
            If there is any unreferred attribute being accessed. This is in addition to the symbol being
            invalid, which is also identified by an AttributeError from the API response
        API error
            Any errors coming from the API, passed on as-is to the caller.
            Any errors coming from the record creation, is also passed on as-is.
        """

        try:
            ticker = yf.Ticker(new_symbol)
            instrument_info = ticker.info

            return self.ingest_new_instrument(instrument_info)
        except AttributeError as error:
            # If the symbol was invalid, ticker.info raises an AttributeError with
            # NoneType in the error message
            if 'NoneType' in error.args[0]:
                raise InvalidTickerSymbolError
            else:
                # If there were any other AttributeError's, we pass them on to the caller of this method
                raise error
        except Exception as exc:
            # If any other error from the API occurs, we pass them on to the caller of this method
            raise exc

    def ingest_new_instrument(self, info: dict):
        """From info create an `Instrument` record

        Pull pre-defined keys from the `info` dict to create values for the record field
        Convert date from epoch time in ms to python date format
        Convert type from the string +Equity+ to its matching label in choices +EQ+

        Parameters
        ----------
        info: dict
            A dictionary containing all the info about the stock as obtained from yfinance API.
            Sample file is at `collectibles/yf_ticker_info_for_symbol.json`

        Returns
        -------
        A record of type `Instrument` as created from the data passed in `info`
        """

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

    def download_historical_data(self, instrument):
        """Downloads historical data & creates DB entries for the instrument passed.

        For a given instrument downloads its historical data till date.
        Stores each day's entry as individual records of `Ohlcv_data`.
        Data downloaded is only for interval=1d, as of now.
        Any rows with any missing information is dropped using `pandas#dropna`
        Not to be used to update an instrument's OHLCV data.
        To be used only for one-time seeding of past data till date.

        Parameters
        ----------
        instrument: Instrument
            The Instrument instance for which historical data is required.

        """

        # TODO: allow range/interval to be passed as an arg to indicate the frequency at which
        # data is desired. Currently one 1d interval is supported.
        ticker = yf.Ticker(instrument.symbol)
        ohlcv_df = ticker.history(
            start=instrument.first_open_date,
        )

        # This DF may have rows with empty values in some columns, dropping rows with any NaN's.
        # This DF has the date as the index, which we need to capture as a column for each entry
        # So we need to reset the index on the DF.
        ohlcv_df = ohlcv_df.reset_index().dropna(how='any')
        ohlcv_df = ohlcv_df.drop(["Volume", "Dividends", "Stock Splits"], axis=1)
        ohlc_df = ohlcv_df.rename(columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
        })
        ohlc_df['date'] = pd.to_datetime(ohlc_df['date']).apply(lambda x: x.to_pydatetime())
        ohlc_df['instrument_id'] = instrument.id

        ohlc_model = self.model.daily_data.rel.related_model
        instrument.daily_data.bulk_create(
            ohlc_model(**vals) for vals in ohlc_df.to_dict('records')
        )
