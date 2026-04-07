from fyers_apiv3 import fyersModel

def view_funds(connect):
    fyers = fyersModel.FyersModel(
        client_id=connect.get("client_id"),
        token=connect.get("access_token"),
        is_async=False,
        log_path="",
    )
    response = fyers.funds()
    return response["fund_limit"][0]["equityAmount"]
