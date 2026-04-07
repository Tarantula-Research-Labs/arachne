from fyers_apiv3 import fyersModel


def place_single_order(connect):
    fyers = fyersModel.FyersModel(
        client_id=connect.get("client_id"),
        token=connect.get("access_token"),
        is_async=False,
        log_path="",
    )
    data = {
        "symbol": "NSE:SBIN-EQ",
        "qty": 5,
        "type": 2,
        "side": 1,
        "productType": "INTRADAY",
        "limitPrice": 0.0030,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,
        "orderTag": "donchian_breakout",
        "isSliceOrder": False,
    }
    response = fyers.place_order(data=data)
    return response
