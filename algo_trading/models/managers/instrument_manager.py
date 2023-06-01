import datetime

import pandas as pd
import yfinance as yf
from django.db import IntegrityError, models
from django.http import Http404

from ...exceptions.instruments.invalid_ticker_symbol_error import (
    InvalidTickerSymbolError,
)


class InstrumentManager(models.Manager):
    KEY_FOR_SYMBOL_IN_INFO = "symbol"
    KEY_FOR_DESCRIPTIVE_NAME_IN_INFO = "longName"
    KEY_FOR_FIRST_OPEN_DATE_IN_INFO = "firstTradeDateMilliseconds"
    KEY_FOR_INSTRUMENT_TYPE_IN_INFO = "typeDisp"

    def get_by_symbol(self, symbol: str):
        """Get an instrument by its symbol, irrespective of case

        Both the queried and the DB column are matched case-insensitive to allow any of the variations:
        RELIANCE.NS, Reliance.NS, RELIANCE.ns, reliancE.nS etc to be mapped to +RELIANCE.NS+

        Parameters
        ----------
        symbol: str
            The symbol to look for

        Raises
        ------
        Http404
            If the symbol cannot be found

        Returns
        -------
        Instrument object
            The instrument matching the symbol, irrespective of case
        """
        try:
            return super().get_queryset().get(trading_symbol__iexact=symbol)
        except self.model.DoesNotExist:
            raise Http404("No Instrument matches the given symbol.")

    def get_options_from_symbol(self, name: str):
        """Get instrument from an option's name

        Specific parsing of options name and conversion from the visible string
        to the internal zerodha format. Zerodha stores the expiry day in the
        trading symbol name, but the call is received with the user friendly
        space separated name without the expiry date. A minor conversion from
        one to the other is done here.

        Parameters
        ----------
        name: str
            The option name, like "ASHOKLEY JUN 145 CE"

        Returns
        -------
        Instrument that has trading symbol "ASHOKLEY23JUN145CE"

        Raises
        ------
        Http404 if the instrument is not found.

        """
        phrases = name.split(" ")
        instrument_name = phrases[0]
        instrument_expiry_and_option = "".join(phrases[1:])

        try:
            return (
                super()
                .get_queryset()
                .filter(trading_symbol__startswith=instrument_name)
                .get(trading_symbol__endswith=instrument_expiry_and_option)
            )
        except self.model.DoesNotExist:
            raise Http404(f"No Option: {name} matches the given symbol.")

    def import_symbols_from_yf(self, symbol_list: list) -> pd.DataFrame:
        """Import multiple symbols from yFinance.

        Given a list of symbols to import, this fetches all their instrument info, and then their
        OHLC historical data from the yfinance API, by calling `import_symbol_from_yf` for each symbol.
        Any errors from importing each symbol is captured and the symbol is stored in the
        failed bucket along with the error msg.
        Any successful import is stored in the created bucket

        Parameters
        ----------
        symbol_list: str
            List of symbols for which to import data

        Returns
        -------
        import_summary: dict[str, list()]
            A dict containing keys +created+ and +failed+
            +created+ key contains a list of Instrument objects that were created
            +failed+ key contains a list of dict with keys +symbol+ and +reason+ containing the error msg.
        """
        import_summary = {}
        failed_symbols = []
        created_symbols = []

        for symbol in symbol_list:
            try:
                created_symbols.append(self.import_symbol_from_yf(symbol))
            except InvalidTickerSymbolError:
                failed_symbols.append({"symbol": symbol, "reason": "Symbol is invalid"})
            except IntegrityError:
                failed_symbols.append(
                    {"symbol": symbol, "reason": "Instrument already exists"}
                )
            except Exception as exc:
                failed_symbols.append({"symbol": symbol, "reason": exc.args})

            # Any possible error for each symbol is handled and an appropriate msg is generated.
            # Whether any one symbol passes or fails, the import continues on for the rest of the symbols.
            continue

        import_summary["failed"] = failed_symbols
        import_summary["created"] = created_symbols

        return import_summary

    def import_symbol_from_yf(self, symbol: str):
        """Import one instrument from YF

        Creates an instrument from the symbol, failing which raises errors
        Downloads historical data for the symbol.

        Parameters
        ----------
        symbol: str
            The symbol to be imported

        Returns
        -------
        ingested_instrument: Instrument
            The Instrument object that got created for the symbol.
        """
        ingested_instrument = self.create_instrument_from_symbol(symbol)
        self.download_historical_data_for(ingested_instrument)

        return ingested_instrument

    def create_instrument_from_symbol(self, new_symbol: str):
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
        IntegrityError
            If the symbol already exists in the database, and is being requested again.
        Exception
            Any errors coming from the API, passed on as-is to the caller.
            Any errors coming from the record creation, is also passed on as-is.
        """

        try:
            ticker = yf.Ticker(new_symbol)

            # A dictionary containing all the info about the stock as obtained from yfinance API.
            # Sample file is at `collectibles/yf_ticker_info_for_symbol.json`
            # @api_method
            instrument_info = ticker.info

            # Normalize API response to model specific formats
            # Convert date from epoch time in ms to python date format
            # Convert type from the string +Equity+ to its matching label in choices +EQ+
            first_open_date_from_info = (
                instrument_info[self.KEY_FOR_FIRST_OPEN_DATE_IN_INFO] / 1000
            )
            first_open_date = datetime.datetime.fromtimestamp(first_open_date_from_info)

            instrument_type_from_info = instrument_info[
                self.KEY_FOR_INSTRUMENT_TYPE_IN_INFO
            ]

            # Convert value from api as 'Equity' to its key 'EQ' from Instrument
            instrument_type = {i.label: i.value for i in self.model.InstrumentType}[
                instrument_type_from_info
            ]  # noqa

            return self.create(
                symbol=instrument_info[self.KEY_FOR_SYMBOL_IN_INFO],
                descriptive_name=instrument_info[self.KEY_FOR_DESCRIPTIVE_NAME_IN_INFO],
                first_open_date=first_open_date,
                instrument_type=instrument_type,
            )
        except AttributeError as error:
            # If the symbol was invalid, ticker.info raises an AttributeError with
            # NoneType in the error message
            if "NoneType" in error.args[0]:
                raise InvalidTickerSymbolError
            else:
                # If there were any other AttributeError's, we pass them on to the caller of this method
                raise error
        except IntegrityError as exc:
            # This happens when a symbol which is already imported is being attempted again
            raise exc
        except Exception as exc:
            # If any other error from the API occurs, we pass them on to the caller of this method
            raise exc

    # @TODO: Needs some lockdown to indicate this is a mutating method
    def download_historical_data_for(self, instrument):
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

        Creates
        -------
            OhlcDataDaily records for each row found in historical data
            Sets their parent record to +instrument+
        """

        # @TODO: allow range/interval to be passed as an arg to indicate the frequency at which
        # data is desired. Currently one 1d interval is supported.
        ticker = yf.Ticker(instrument.symbol)
        ohlc_df = ticker.history(
            start=instrument.first_open_date,
        )

        # This DF may have rows with empty values in some columns, dropping rows with any NaN's.
        # This DF has the date as the index, which we need to capture as a column for each entry
        # So we need to reset the index on the DF.
        ohlc_df = ohlc_df.reset_index().dropna(how="any")
        ohlc_df = ohlc_df.drop(["Volume", "Dividends", "Stock Splits"], axis=1)
        ohlc_df = ohlc_df.rename(
            columns={
                "Date": "date",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
            }
        )
        ohlc_df["date"] = pd.to_datetime(ohlc_df["date"]).apply(
            lambda x: x.to_pydatetime()
        )
        ohlc_df["instrument_id"] = instrument.id

        daily_data_rel = instrument.daily_data
        daily_data_rel.bulk_create(
            daily_data_rel.model(**vals) for vals in ohlc_df.to_dict("records")
        )

    def load_bulk_instruments(self, instruments_from_exchange: list) -> list:
        """Loads instruments available from the exchange into our DB.

        Given an array of instruments, they're loaded into our DB if they're not present already.
        Existing instruments are skipped over. This is applicable for Zerodha's API
        endpoint +/instruments+

        Parameters
        ----------
        instruments_from_exchange: Array<dict>
            Array of objects containing count of the instruments that are imported

        Creates
        -------
        All instrument objects with the data coming from the payload. Only new objects
        are created. Already existing objects (identified by duplicate pairs of
        trading_symbol and exchange) are skipped over and not imported.

        Returns
        -------
        Count of all instruments either created or found
        """
        created_instruments = 0

        for instrument_info in instruments_from_exchange:
            instrument_info["symbol"] = instrument_info["tradingsymbol"]
            instrument_info["trading_symbol"] = instrument_info["tradingsymbol"]
            del instrument_info["tradingsymbol"]
            del instrument_info["last_price"]

            try:
                self.create(**instrument_info)
                created_instruments += 1
            except IntegrityError:
                pass

        return created_instruments
