from fyers_apiv3 import fyersModel
from authentication import get_access_token

def view_funds(connect):
    fyers = fyersModel.FyersModel(
        client_id=connect.get("client_id"),
        token=get_access_token(),
        is_async=False,
        log_path="",
    )
    response = fyers.funds()
    return response["fund_limit"][0]["equityAmount"]
