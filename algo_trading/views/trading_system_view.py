from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from ..forms.zerodha.options_call_form import OptionsCallForm
from ..models.business_domain.trading_system import TradingSystem


@require_http_methods(["GET", "POST"])
def place_options_call(request):
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


# 'call_blob': ['TATACHEM JUN 970 CE\r\nEntry -  18\r\nTargets -  22, 40+\r\nStoploss -  9']
