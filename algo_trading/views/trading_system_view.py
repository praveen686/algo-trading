from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from ..forms.zerodha.options_call_form import OptionsCallForm
from ..models.business_domain.trading_system import TradingSystem


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
    """

    # @TODO
    # check if duplicate call is placed with the same params accidentally.
    ts = TradingSystem()
    trading_signal = None

    if request.method == "POST":
        options_call_form = OptionsCallForm(request.POST)

        if options_call_form.is_valid():
            trading_signal = ts.place_order_from_call_blob(
                options_call_form.cleaned_data["call_blob"]
            )
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
