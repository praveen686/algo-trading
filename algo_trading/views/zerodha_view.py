from django.shortcuts import redirect
from django.utils.http import urlencode
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

from ..models.kite_broker import KiteBroker


ZERODHA_API_KEY = "g54suy4ucztqh9se"
ZERODHA_API_SECRET = "i637gje20mtuxco4kczs8uc666ogpsop"


@require_http_methods(["GET"])
def zerodha_login_url(request):
    kite = KiteBroker(api_key=ZERODHA_API_KEY)
    redirect_string = "&redirect_params=" + urlencode({'redirect_to': request.GET.get('next')})
    return JsonResponse({'zerodha_login_url': kite.login_url() + redirect_string})


@ensure_csrf_cookie
@require_http_methods(["GET"])
def zerodha_req_token(request):
    zerodha_request_token = request.GET.get('request_token')
    # todo add handler if token is nil or status/success is false
    kite = KiteBroker(api_key=ZERODHA_API_KEY)

    data = kite.generate_session(zerodha_request_token, api_secret=ZERODHA_API_SECRET)
    kite.set_access_token(data["access_token"])

    profile = kite.profile()

    print(f"*******{profile}")
    print(f"**** next is {request.GET.get('redirect_to')}")
    return redirect(request.GET.get('redirect_to'))
