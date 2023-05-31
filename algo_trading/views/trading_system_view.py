from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from ..forms.zerodha.options_call_form import OptionsCallForm
from ..models.kite_broker import KiteBroker


@require_http_methods(["GET", "POST"])
def place_options_call(request):
    kite = KiteBroker()
    print(f"form data={request.POST}")
    if request.method == "POST":
        options_call_form = OptionsCallForm(request.POST)

        if options_call_form.is_valid():
            (
                option_name,
                entry_price,
                stoploss_price,
                target1_price,
                target2_price,
            ) = kite.parse_call_from_blob(options_call_form.cleaned_data["call_blob"])

    else:
        options_call_form = OptionsCallForm()

    return render(
        request,
        "trading_system/place_options_call.html",
        {
            "form": options_call_form,
        },
    )


# 'call_blob': ['TATACHEM JUN 970 CE\r\nEntry -  18\r\nTargets -  22, 40+\r\nStoploss -  9']
