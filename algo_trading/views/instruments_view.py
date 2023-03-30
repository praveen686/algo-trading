# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from ..models import Instrument

from ..forms import AddInstrumentForm


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
            return attempt_add_new_instrument(form)
    else:
        form = AddInstrumentForm()

    return render(request, 'instruments/add_instrument.html', {'form': form})


def attempt_add_new_instrument(form):
    requested_symbol = form.cleaned_data['symbol']
    # try:
    #     Instrument.process_new_instrument(requested_symbol)
    # except ImportError:
    #     form.error_messages = 'The requested symbol is invalid'
