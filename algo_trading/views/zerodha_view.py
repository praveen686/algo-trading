from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.http import urlencode
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from ..models.kite_broker import KiteBroker


@require_http_methods(["GET"])
def zerodha_login_url(request):
    kite = KiteBroker()
    redirect_string = "&redirect_params=" + urlencode(
        {"redirect_to": request.GET.get("next")}
    )
    return JsonResponse({"zerodha_login_url": kite.login_url() + redirect_string})


@ensure_csrf_cookie
@require_http_methods(["GET"])
def zerodha_req_token(request):
    zerodha_request_token = request.GET.get("request_token")
    # todo add handler if token is nil or status/success is false
    kite = KiteBroker()

    data = kite.create_session(zerodha_request_token)
    kite.set_access_token(data["access_token"])
    kite.set_refresh_token(data["refresh_token"])

    return redirect(request.GET.get("redirect_to"))


def zerodha_instruments(request):
    kite = KiteBroker()

    count = kite.load_instruments_for_today()

    return JsonResponse({"size": count})
