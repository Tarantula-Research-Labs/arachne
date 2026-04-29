from fyers_apiv3 import fyersModel
from authentication import get_access_token

def exit_position(connect):
    fyers = fyersModel.FyersModel(
        client_id=connect.get("client_id"),
        token=get_access_token(),
        is_async=False,
        log_path="",
    )
    data = {
        "segment":[10],
        "side":[1,-1],
        "productType":["INTRADAY"]
       }

    response = fyers.exit_positions(data=data)
    return response