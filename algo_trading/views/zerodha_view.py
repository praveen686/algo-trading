from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.http import urlencode
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from ..models.business_domain.kite_broker import KiteBroker


@require_http_methods(["GET"])
def zerodha_login_url(request):
    """Returns the login url for the zerodha client"""

    kite = KiteBroker()
    redirect_string = "&redirect_params=" + urlencode(
        {"redirect_to": request.GET.get("next")}
    )
    return JsonResponse({"zerodha_login_url": kite.login_url() + redirect_string})


@ensure_csrf_cookie
@require_http_methods(["GET"])
def zerodha_req_token(request):
    """Endpoint for receiving the successful login from Zerodha

    When a successful login and authorization with the Zerodha client happens from the
    UI, this endpoint is called by the zerodha app with the request token as a query
    parameter and an additional param called `redirect_to` which is sent by us with
    the login request to indicate which page this login was called from.

    Creates a session with the request token, receiving an access token from Zerodha
    in the process, and setting that in the kite broker client to facilitate
    further api calls. Also sets the refresh token for future uses. Unused for now.

    Redirects the user back to the page from where the login button on the UI
    was clicked.
    """
    zerodha_request_token = request.GET.get("request_token")
    # todo add handler if token is nil or status/success is false
    kite = KiteBroker()

    data = kite.create_session(zerodha_request_token)
    kite.set_access_token(data["access_token"])
    print(f"******* KAT = {data['access_token']}")
    kite.set_refresh_token(data["refresh_token"])

    return redirect(request.GET.get("redirect_to"))


def zerodha_instruments(request):
    """View action for loading all instruments from Zerodha

    Provided as a convenience/testing method to see if the import from
    Zerodha is working correctly and importing the updated instrument list, if any.

    Returns a `JsonResponse` with the count of instruments imported per exchange
    """
    kite = KiteBroker()

    count_by_exchange = kite.load_instruments_for_today()

    return JsonResponse(count_by_exchange, safe=False)
