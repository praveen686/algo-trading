# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from ..models import Instrument


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
