# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from ..models import Instrument

from ..forms import AddInstrumentForm
from ..exceptions import InvalidTickerSymbolError


@require_http_methods(["GET"])
def instrument_by_pk(request, pk: int):
    instrument = get_object_or_404(Instrument, pk=pk)
    return display_instrument(
        request,
        instrument
    )


@require_http_methods(["GET"])
def instrument_by_symbol(request, symbol: str):
    instrument = get_object_or_404(Instrument, symbol=symbol)
    return display_instrument(
        request,
        instrument
    )


def display_instrument(request, instrument: Instrument):
    return render(
        request,
        'instruments/show.html',
        {
            'instrument': instrument,
        },
    )


@require_http_methods(["GET", "POST"])
def add_instruments(request):
    if request.method == 'POST':
        form = AddInstrumentForm(request.POST)

        if form.is_valid():
            new_instrument = attempt_add_new_instrument(form)
            if new_instrument is not None:
                return redirect(new_instrument)
    else:
        form = AddInstrumentForm()

    return render(request, 'instruments/add_instrument.html', {'form': form})


def attempt_add_new_instrument(form):
    try:
        new_instrument = Instrument.objects.process_new_instrument(form.cleaned_data['symbol'])
        Instrument.objects.download_historical_data([new_instrument])
        return new_instrument
    except InvalidTickerSymbolError:
        form.add_error('symbol', 'The requested symbol is invalid. No ticker info found.')
    except Exception as exception:
        form.add_error(None, exception.args)
