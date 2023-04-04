# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from ..models import Instrument

from ..forms import AddInstrumentForm
from ..exceptions import InvalidTickerSymbolError


@require_http_methods(["GET"])
def instrument_by_pk(request, pk: int):
    """Show an `Instrument` instance identified by its primary key: `pk`"""

    instrument = get_object_or_404(Instrument, pk=pk)
    return display_instrument(
        request,
        instrument
    )


@require_http_methods(["GET"])
def instrument_by_symbol(request, symbol: str):
    """Show an `Instrument` instance identified by its `symbol`"""

    instrument = get_object_or_404(Instrument, symbol=symbol)
    return display_instrument(
        request,
        instrument
    )


def display_instrument(request, instrument: Instrument):
    """Common function to show an `Instrument`"""

    return render(
        request,
        'instruments/show.html',
        {
            'instrument': instrument,
        },
    )


@require_http_methods(["GET", "POST"])
def add_instruments(request):
    """Add an instrument into the system

    Uses a form modeled on the `Instrument` class and uses only the field `symbol`
    The form is validated against the model and at the HTTP level
    If the request was a GET, it means user navigated to this page, so we show an empty form.
    The empty form prompts the user to enter the symbol that needs to be added to our system
    If the request was a POST, it means user typed in the symbol and submitted the form.
    A new record is attempted to be created from the symbol.
    If the symbol is correct, and no API failure happens, the symbol is added and navigation
    directed to that Instrument's show page.
    If the symbol is incorrect or an API failure happens, relevant error message is shown on the form.
    """

    if request.method == 'POST':
        form = AddInstrumentForm(request.POST)

        if form.is_valid():
            new_instrument = attempt_add_new_instrument(form)
            if new_instrument is not None:
                return redirect(new_instrument)
    else:
        form = AddInstrumentForm()

    return render(request, 'instruments/add_instrument.html', {'form': form})


def attempt_add_new_instrument(form: AddInstrumentForm) -> Instrument:
    """Tries to create a new instrument from the form data.

    Internal function for the view, not to be called from outside.
    Processes the symbol through the yfinance API to collect basic info about the stock
    and creates a new Instrument instance from that info
    For the newly created Instrument, downloads all historical data till date and creates
    a record of type _FILLME_ for every available date in the historical data with their
    OHLCV entries.

    Parameters
    ----------
    form: AddInstrumentForm
        An instance of AddInstrumentForm bound with the POST data from the request

    Returns
    ----------
    new_instrument: Instrument
        The new `Instrument` instance that was created with the form data, a la, the symbol

    Raises
    ------
    Adds errors to the form on the field `symbol` if it was invalid,
    or to the general non-form-field if there were any other API/model level errors
    """

    try:
        new_instrument = Instrument.objects.process_new_instrument(form.cleaned_data['symbol'])
        Instrument.objects.download_historical_data(new_instrument)
        return new_instrument
    except InvalidTickerSymbolError:
        form.add_error('symbol', 'The requested symbol is invalid. No ticker info found.')
    except Exception as exception:
        form.add_error(None, exception.args)
