from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from ..forms.zerodha.options_call_form import OptionsCallForm
from ..models.business_domain.trading_system import TradingSystem
from ..models.trading_signal import TradingSignal


@require_http_methods(["GET", "POST"])
def place_options_call(request):
    """Creates an option call via a TradingSignal object

    The POST request has the details of the call as received.
    Parses that to create a signal and places an order.
    Alerts the user if the same call was placed more than once
    Raises an error if the instrument is not found in the DB.

    Raises
    ------
    Error404 if the requested instrument does not exist in the list of instruments
    to trade from the daily zerodha import.

    Redirects to
    ------------
    Created trading Signal page, which will also have the order object.
    """

    # @TODO
    # check if duplicate call is placed with the same params accidentally.

    ts = TradingSystem()
    trading_signal = None

    if request.method == "POST":
        options_call_form = OptionsCallForm(request.POST)

        if options_call_form.is_valid():
            (trading_signal, order) = ts.place_order_from_call_blob(
                options_call_form.cleaned_data["call_blob"]
            )
            return redirect(trading_signal)
    else:
        options_call_form = OptionsCallForm()

    return render(
        request,
        "trading_system/place_options_call.html",
        {
            "form": options_call_form,
            "signal": trading_signal,
        },
    )


@require_http_methods(["GET"])
def trading_signal(request, pk: int):
    """Show a trading signal"""

    trading_signal = get_object_or_404(TradingSignal, pk=pk)

    return render(
        request,
        "trading_system/trading_signal.html",
        {"trading_signal": trading_signal},
    )


@require_http_methods(["GET"])
def options_calls(request):
    """Show all options calls"""

    options_calls = TradingSignal.objects.get_options_calls()

    return render(
        request,
        "trading_system/options_calls.html",
        {"options_calls": options_calls},
    )
